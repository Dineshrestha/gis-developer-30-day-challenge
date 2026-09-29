"""Generate deterministic synthetic data for Day 01.

Scenario
--------
Client XYZ sends a recurring field-inspection Excel delivery. Before the GIS
production team uses it, the delivery must be validated against the
organization's authoritative GIS asset inventory.

Outputs
-------
data/sample/authoritative_assets.geojson
data/sample/xyz_field_delivery.xlsx

All data are synthetic. A fixed random seed makes the exercise reproducible.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
rng = np.random.default_rng(SEED)

HERE = Path(__file__).resolve().parent
SAMPLE_DIR = HERE / "sample"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

ASSET_COUNT = 1000
DELIVERY_COUNT = 300

ASSET_TYPES = ["Valve", "Meter", "Regulator", "Pump", "Sensor", "Station"]
STATUSES = ["Active", "Inactive", "Maintenance"]
PRIORITIES = ["Low", "Medium", "High"]
INSPECTORS = ["A. Rivera", "J. Chen", "M. Patel", "S. Brooks", "L. Nguyen", "R. Gomez"]
REGIONS = ["North", "Central", "South"]
DISTRICTS = {
    "North": ["N-01", "N-02", "N-03"],
    "Central": ["C-01", "C-02", "C-03"],
    "South": ["S-01", "S-02", "S-03"],
}


def random_dates(start: str, end: str, n: int) -> pd.Series:
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    offsets = rng.integers(0, (end_ts - start_ts).days + 1, size=n)
    return pd.Series(start_ts + pd.to_timedelta(offsets, unit="D"))


# ---------------------------------------------------------------------------
# Authoritative GIS asset inventory
# ---------------------------------------------------------------------------
asset_ids = [f"AST-{i:04d}" for i in range(1, ASSET_COUNT + 1)]
regions = rng.choice(REGIONS, size=ASSET_COUNT)
authoritative = pd.DataFrame(
    {
        "asset_id": asset_ids,
        "asset_type": rng.choice(ASSET_TYPES, size=ASSET_COUNT),
        "status": rng.choice(STATUSES, size=ASSET_COUNT, p=[0.82, 0.08, 0.10]),
        "priority": rng.choice(PRIORITIES, size=ASSET_COUNT, p=[0.30, 0.48, 0.22]),
        "region": regions,
        "district": [rng.choice(DISTRICTS[r]) for r in regions],
        "inspector": rng.choice(INSPECTORS, size=ASSET_COUNT),
        "install_date": random_dates("2010-01-01", "2024-12-31", ASSET_COUNT).dt.strftime("%Y-%m-%d"),
        "last_inspection": random_dates("2025-01-01", "2026-08-31", ASSET_COUNT).dt.strftime("%Y-%m-%d"),
        "condition_score": rng.integers(45, 101, size=ASSET_COUNT),
        "pressure_psi": np.round(rng.uniform(35, 125, size=ASSET_COUNT), 1),
        "longitude": np.round(rng.uniform(-97.55, -97.05, size=ASSET_COUNT), 6),
        "latitude": np.round(rng.uniform(32.55, 32.95, size=ASSET_COUNT), 6),
    }
)

features = []
for record in authoritative.to_dict(orient="records"):
    props = {k: v for k, v in record.items() if k not in {"longitude", "latitude"}}
    features.append(
        {
            "type": "Feature",
            "properties": props,
            "geometry": {
                "type": "Point",
                "coordinates": [record["longitude"], record["latitude"]],
            },
        }
    )

geojson = {
    "type": "FeatureCollection",
    "name": "authoritative_assets",
    "features": features,
}
(SAMPLE_DIR / "authoritative_assets.geojson").write_text(
    json.dumps(geojson, indent=2), encoding="utf-8"
)

auth = authoritative.set_index("asset_id").to_dict(orient="index")
rows: list[dict] = []


def next_record_id() -> str:
    return f"XYZ-20260928-{len(rows) + 1:04d}"


def base_row(asset_id: str) -> dict:
    a = auth[asset_id]
    return {
        "client_record_id": next_record_id(),
        "asset_id": asset_id,
        "status_new": a["status"],
        "priority_new": a["priority"],
        "inspector_new": a["inspector"],
        "inspection_date": a["last_inspection"],
        "condition_score_new": a["condition_score"],
        "pressure_psi_new": a["pressure_psi"],
        "comments": "",
        "scenario_expected": "",
    }


def newer(asset_id: str, days: int = 10) -> str:
    d = pd.Timestamp(auth[asset_id]["last_inspection"]) + pd.Timedelta(days=days)
    return min(d, pd.Timestamp("2026-09-28")).strftime("%Y-%m-%d")


def older(asset_id: str, days: int = 30) -> str:
    return (
        pd.Timestamp(auth[asset_id]["last_inspection"]) - pd.Timedelta(days=days)
    ).strftime("%Y-%m-%d")


# 200 valid changed records. The first 10 also test ID normalization.
for i in range(1, 201):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    if i <= 10:
        row["asset_id"] = f"  {aid.lower()}  "
    row["inspection_date"] = newer(aid, int(rng.integers(1, 28)))
    row["condition_score_new"] = max(0, min(100, int(auth[aid]["condition_score"]) - 3))
    if row["condition_score_new"] == auth[aid]["condition_score"]:
        row["condition_score_new"] = max(0, row["condition_score_new"] - 1)
    if i % 3 == 0:
        row["priority_new"] = {"Low": "Medium", "Medium": "High", "High": "Medium"}[auth[aid]["priority"]]
    row["comments"] = "Routine field inspection update"
    row["scenario_expected"] = "READY_TO_UPDATE"
    rows.append(row)

# 20 valid records with no actual changes.
for i in range(201, 221):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    row["comments"] = "Field inspection confirms existing values"
    row["scenario_expected"] = "NO_CHANGE"
    rows.append(row)

# 10 partial updates: blanks must preserve authoritative GIS values.
for i in range(221, 231):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    row.update(
        {
            "status_new": "",
            "priority_new": "",
            "inspector_new": "",
            "inspection_date": newer(aid, 7),
            "condition_score_new": max(0, int(auth[aid]["condition_score"]) - 5),
            "pressure_psi_new": "",
            "comments": "Partial update; blank values should not erase GIS values",
            "scenario_expected": "READY_TO_UPDATE",
        }
    )
    rows.append(row)

# 20 stale inspection records.
for i in range(231, 251):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    row["inspection_date"] = older(aid, 45)
    row["priority_new"] = "High"
    row["comments"] = "Older inspection received after newer authoritative record"
    row["scenario_expected"] = "REJECTED_STALE"
    rows.append(row)

# 10 invalid priority-domain records.
for i in range(251, 261):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    row["inspection_date"] = newer(aid, 10)
    row["priority_new"] = "Urgent"
    row["comments"] = "Intentional invalid priority domain"
    row["scenario_expected"] = "REJECTED_DOMAIN"
    rows.append(row)

# 5 invalid numeric-range records.
for i in range(261, 266):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    row["inspection_date"] = newer(aid, 10)
    row["condition_score_new"] = 150
    row["comments"] = "Intentional out-of-range condition score"
    row["scenario_expected"] = "REJECTED_RANGE"
    rows.append(row)

# 5 malformed dates.
for i in range(266, 271):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    row["inspection_date"] = "09/31/2026"
    row["comments"] = "Intentional malformed inspection date"
    row["scenario_expected"] = "REJECTED_DATE"
    rows.append(row)

# 5 null asset IDs.
for i in range(271, 276):
    aid = f"AST-{i:04d}"
    row = base_row(aid)
    row["asset_id"] = None
    row["inspection_date"] = newer(aid, 10)
    row["comments"] = "Intentional missing asset ID"
    row["scenario_expected"] = "REJECTED_NULL_ID"
    rows.append(row)

# 10 rows forming five duplicate-ID pairs.
for i in range(276, 281):
    aid = f"AST-{i:04d}"
    for n, priority in enumerate(["High", "Low"], start=1):
        row = base_row(aid)
        row["inspection_date"] = newer(aid, 10 + n)
        row["priority_new"] = priority
        row["comments"] = f"Intentional duplicate pair - row {n}"
        row["scenario_expected"] = "REJECTED_DUPLICATE"
        rows.append(row)

# 15 records whose IDs do not exist in authoritative GIS.
for i in range(1, 16):
    rows.append(
        {
            "client_record_id": next_record_id(),
            "asset_id": f"AST-{2000 + i:04d}",
            "status_new": "Active",
            "priority_new": rng.choice(PRIORITIES),
            "inspector_new": rng.choice(INSPECTORS),
            "inspection_date": "2026-09-20",
            "condition_score_new": int(rng.integers(60, 96)),
            "pressure_psi_new": float(np.round(rng.uniform(40, 120), 1)),
            "comments": "Asset not found in authoritative GIS",
            "scenario_expected": "UNMATCHED",
        }
    )

delivery = pd.DataFrame(rows)
assert len(delivery) == DELIVERY_COUNT, f"Expected {DELIVERY_COUNT}, got {len(delivery)}"

# Mix issue types throughout the workbook.
delivery = delivery.sample(frac=1, random_state=SEED).reset_index(drop=True)

xlsx_path = SAMPLE_DIR / "xyz_field_delivery.xlsx"
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
    delivery.to_excel(writer, sheet_name="Field_Delivery", index=False)
    (
        delivery["scenario_expected"]
        .value_counts()
        .rename_axis("expected_status")
        .reset_index(name="record_count")
        .to_excel(writer, sheet_name="Expected_Test_Counts", index=False)
    )

print("Day 01 synthetic corporate data created successfully.")
print(f"Authoritative GIS assets: {ASSET_COUNT}")
print(f"Client XYZ delivery rows: {DELIVERY_COUNT}")
print(delivery["scenario_expected"].value_counts().sort_index().to_string())
