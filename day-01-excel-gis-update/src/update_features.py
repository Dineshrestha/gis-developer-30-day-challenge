"""Reusable validation and GIS reconciliation logic for Day 01.

The module separates data-quality decisions from ArcPy editing so most of the
workflow can be tested with pandas before any GIS feature is modified.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd


def load_rules(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_asset_id(value: Any) -> str | None:
    """Normalize client IDs before matching: strip whitespace and uppercase."""
    if pd.isna(value):
        return None
    text = str(value).strip().upper()
    return text or None


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = sorted(set(required_columns) - set(df.columns))
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))


def read_feature_class(feature_class: str | Path) -> pd.DataFrame:
    """Read authoritative ArcGIS attributes into a DataFrame."""
    import arcpy

    fields = [
        "asset_id",
        "asset_type",
        "status",
        "priority",
        "region",
        "district",
        "inspector",
        "install_date",
        "last_inspection",
        "condition_score",
        "pressure_psi",
    ]
    rows = list(arcpy.da.SearchCursor(str(feature_class), fields))
    return pd.DataFrame(rows, columns=fields)


def _is_blank(value: Any) -> bool:
    return pd.isna(value) or (isinstance(value, str) and not value.strip())


def _normalize_compare(value: Any, field_name: str) -> Any:
    if _is_blank(value):
        return None
    if "date" in field_name or field_name == "last_inspection":
        parsed = pd.to_datetime(value, errors="coerce")
        return None if pd.isna(parsed) else parsed.strftime("%Y-%m-%d")
    if field_name in {"condition_score", "condition_score_new"}:
        return int(float(value))
    if field_name in {"pressure_psi", "pressure_psi_new"}:
        return round(float(value), 1)
    return str(value).strip()


def reconcile_delivery(
    incoming: pd.DataFrame,
    authoritative: pd.DataFrame,
    rules: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Validate, match, classify, and audit a client delivery."""
    start = perf_counter()
    validate_required_columns(incoming, rules["required_columns"])

    work = incoming.copy()
    work["asset_id_normalized"] = work[rules["id_field"]].map(normalize_asset_id)
    work["validation_status"] = "PENDING"
    work["validation_reason"] = ""

    authoritative = authoritative.copy()
    authoritative["asset_id_normalized"] = authoritative["asset_id"].map(normalize_asset_id)
    authoritative_lookup = authoritative.set_index("asset_id_normalized", drop=False).to_dict(orient="index")

    def reject(mask: pd.Series, status: str, reason: str) -> None:
        eligible = mask & work["validation_status"].eq("PENDING")
        work.loc[eligible, "validation_status"] = status
        work.loc[eligible, "validation_reason"] = reason

    reject(work["asset_id_normalized"].isna(), "REJECTED", "Missing asset_id")

    duplicate_mask = work["asset_id_normalized"].notna() & work["asset_id_normalized"].duplicated(keep=False)
    reject(duplicate_mask, "REJECTED", "Duplicate asset_id in client delivery")

    pattern = re.compile(rules["id_pattern"])
    invalid_format = work["asset_id_normalized"].notna() & ~work["asset_id_normalized"].map(
        lambda x: bool(pattern.fullmatch(x)) if x else False
    )
    reject(invalid_format, "REJECTED", "asset_id does not match organization format")

    for field, allowed in rules.get("allowed_values", {}).items():
        nonblank = ~work[field].map(_is_blank)
        invalid = nonblank & ~work[field].isin(allowed)
        reject(invalid, "REJECTED", f"Invalid {field}; allowed values: {', '.join(allowed)}")

    raw_dates = work["inspection_date"].copy()
    parsed_dates = pd.to_datetime(raw_dates, errors="coerce")
    invalid_dates = (~raw_dates.map(_is_blank)) & parsed_dates.isna()
    reject(invalid_dates, "REJECTED", "Invalid inspection_date")
    work["inspection_date_parsed"] = parsed_dates

    for field, bounds in rules.get("numeric_ranges", {}).items():
        raw = work[field]
        nonblank = ~raw.map(_is_blank)
        numeric = pd.to_numeric(raw, errors="coerce")
        invalid_type = nonblank & numeric.isna()
        reject(invalid_type, "REJECTED", f"{field} is not numeric")
        low, high = bounds
        out_of_range = nonblank & numeric.notna() & ~numeric.between(low, high)
        reject(out_of_range, "REJECTED", f"{field} outside allowed range {low}–{high}")
        work[field] = numeric.where(nonblank, pd.NA)

    matched_mask = work["asset_id_normalized"].isin(authoritative_lookup)
    reject(~matched_mask, "UNMATCHED", "asset_id not found in authoritative GIS")

    if rules.get("reject_stale_inspection_dates", True):
        stale = pd.Series(False, index=work.index)
        pending_matched = work["validation_status"].eq("PENDING") & matched_mask
        for idx in work.index[pending_matched]:
            aid = work.at[idx, "asset_id_normalized"]
            incoming_date = work.at[idx, "inspection_date_parsed"]
            existing_date = pd.to_datetime(authoritative_lookup[aid]["last_inspection"], errors="coerce")
            if pd.notna(incoming_date) and pd.notna(existing_date):
                stale.at[idx] = incoming_date < existing_date
        reject(stale, "REJECTED", "Incoming inspection is older than authoritative GIS")

    audit_rows: list[dict[str, Any]] = []
    pending_rows = work.index[work["validation_status"].eq("PENDING")]

    for idx in pending_rows:
        aid = work.at[idx, "asset_id_normalized"]
        existing = authoritative_lookup[aid]
        row_changes = 0

        for incoming_field, gis_field in rules["field_mapping"].items():
            incoming_value = work.at[idx, incoming_field]
            if rules.get("blank_values_preserve_existing", True) and _is_blank(incoming_value):
                continue

            old_value = _normalize_compare(existing[gis_field], gis_field)
            new_value = _normalize_compare(incoming_value, incoming_field)

            if old_value != new_value:
                row_changes += 1
                audit_rows.append(
                    {
                        "client_record_id": work.at[idx, "client_record_id"],
                        "asset_id": aid,
                        "field": gis_field,
                        "old_value": old_value,
                        "new_value": new_value,
                    }
                )

        if row_changes:
            work.at[idx, "validation_status"] = "READY_TO_UPDATE"
            work.at[idx, "validation_reason"] = f"{row_changes} field change(s)"
        else:
            work.at[idx, "validation_status"] = "NO_CHANGE"
            work.at[idx, "validation_reason"] = "Valid record; no attribute changes detected"

    audit = pd.DataFrame(
        audit_rows,
        columns=["client_record_id", "asset_id", "field", "old_value", "new_value"],
    )

    work["asset_id"] = work["asset_id_normalized"].where(
        work["asset_id_normalized"].notna(), work["asset_id"]
    )

    status_counts = work["validation_status"].value_counts().to_dict()
    received = len(work)
    ready = int(status_counts.get("READY_TO_UPDATE", 0))
    no_change = int(status_counts.get("NO_CHANGE", 0))
    rejected = int(status_counts.get("REJECTED", 0))
    unmatched = int(status_counts.get("UNMATCHED", 0))
    accepted = ready + no_change
    quality_score = round((accepted / received * 100), 1) if received else 0.0

    summary = {
        "client": rules.get("client_name", "Unknown"),
        "records_received": received,
        "ready_to_update": ready,
        "no_change": no_change,
        "rejected": rejected,
        "unmatched": unmatched,
        "accepted_records": accepted,
        "data_quality_score_pct": quality_score,
        "field_changes": len(audit),
        "processing_seconds": round(perf_counter() - start, 3),
        "delivery_status": "READY FOR GIS" if rejected == 0 and unmatched == 0 else "REVIEW REQUIRED",
    }

    return work, audit, summary


def split_reports(classified: pd.DataFrame, audit: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "Ready_to_Update": classified[classified["validation_status"].eq("READY_TO_UPDATE")].copy(),
        "Rejected": classified[classified["validation_status"].eq("REJECTED")].copy(),
        "Unmatched": classified[classified["validation_status"].eq("UNMATCHED")].copy(),
        "No_Change": classified[classified["validation_status"].eq("NO_CHANGE")].copy(),
        "Change_Audit": audit.copy(),
    }


def write_csv_reports(reports: dict[str, pd.DataFrame], output_dir: str | Path) -> dict[str, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name, df in reports.items():
        path = output_dir / f"{name.lower()}.csv"
        df.to_csv(path, index=False)
        paths[name] = path
    return paths


def apply_updates_to_feature_class(
    feature_class: str | Path,
    ready_records: pd.DataFrame,
    rules: dict[str, Any],
) -> int:
    """Apply only READY_TO_UPDATE records to a local ArcGIS feature class."""
    import arcpy

    if ready_records.empty:
        return 0

    update_lookup = ready_records.set_index("asset_id_normalized").to_dict(orient="index")
    gis_fields = [rules["id_field"]] + list(rules["field_mapping"].values())
    incoming_fields = list(rules["field_mapping"].keys())
    field_types = {f.name: f.type for f in arcpy.ListFields(str(feature_class))}

    updated = 0
    with arcpy.da.UpdateCursor(str(feature_class), gis_fields) as cursor:
        for row in cursor:
            aid = normalize_asset_id(row[0])
            if aid not in update_lookup:
                continue

            incoming = update_lookup[aid]
            changed = False

            for pos, incoming_field in enumerate(incoming_fields, start=1):
                value = incoming[incoming_field]
                if rules.get("blank_values_preserve_existing", True) and _is_blank(value):
                    continue

                if incoming_field == "inspection_date":
                    target_field = rules["field_mapping"][incoming_field]
                    parsed = pd.to_datetime(value)
                    value = (
                        parsed.to_pydatetime()
                        if field_types.get(target_field) == "Date"
                        else parsed.strftime("%Y-%m-%d")
                    )
                elif incoming_field == "condition_score_new":
                    value = int(value)
                elif incoming_field == "pressure_psi_new":
                    value = float(value)

                if row[pos] != value:
                    row[pos] = value
                    changed = True

            if changed:
                cursor.updateRow(row)
                updated += 1

    return updated
