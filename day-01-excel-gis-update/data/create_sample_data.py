"""Create reproducible synthetic data for Day 01.

Outputs
-------
data/sample/infrastructure_assets.geojson
    Synthetic point features representing infrastructure assets.

data/sample/incoming_updates.xlsx
    Excel workbook containing one normal update sheet plus several
    intentionally bad sheets used to test validation behavior.

All records are synthetic and safe to publish.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
SAMPLE_DIR = HERE / "sample"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# 1. Synthetic GIS assets
# -----------------------------------------------------------------------------
assets = [
    {
        "asset_id": "AST-001",
        "asset_type": "Valve",
        "status": "Active",
        "priority": "Medium",
        "inspector": "A. Rivera",
        "last_inspection": "2026-07-15",
        "longitude": -97.3400,
        "latitude": 32.7600,
    },
    {
        "asset_id": "AST-002",
        "asset_type": "Valve",
        "status": "Active",
        "priority": "Low",
        "inspector": "A. Rivera",
        "last_inspection": "2026-07-18",
        "longitude": -97.3320,
        "latitude": 32.7650,
    },
    {
        "asset_id": "AST-003",
        "asset_type": "Meter",
        "status": "Active",
        "priority": "Medium",
        "inspector": "J. Chen",
        "last_inspection": "2026-06-29",
        "longitude": -97.3250,
        "latitude": 32.7700,
    },
    {
        "asset_id": "AST-004",
        "asset_type": "Regulator",
        "status": "Active",
        "priority": "High",
        "inspector": "J. Chen",
        "last_inspection": "2026-06-20",
        "longitude": -97.3180,
        "latitude": 32.7750,
    },
    {
        "asset_id": "AST-005",
        "asset_type": "Meter",
        "status": "Inactive",
        "priority": "Low",
        "inspector": "M. Patel",
        "last_inspection": "2026-05-11",
        "longitude": -97.3110,
        "latitude": 32.7800,
    },
    {
        "asset_id": "AST-006",
        "asset_type": "Valve",
        "status": "Active",
        "priority": "Medium",
        "inspector": "M. Patel",
        "last_inspection": "2026-08-02",
        "longitude": -97.3040,
        "latitude": 32.7850,
    },
    {
        "asset_id": "AST-007",
        "asset_type": "Regulator",
        "status": "Active",
        "priority": "Low",
        "inspector": "S. Brooks",
        "last_inspection": "2026-08-10",
        "longitude": -97.2970,
        "latitude": 32.7900,
    },
    {
        "asset_id": "AST-008",
        "asset_type": "Meter",
        "status": "Active",
        "priority": "Medium",
        "inspector": "S. Brooks",
        "last_inspection": "2026-08-17",
        "longitude": -97.2900,
        "latitude": 32.7950,
    },
]

features = []
for asset in assets:
    properties = {
        key: value
        for key, value in asset.items()
        if key not in {"longitude", "latitude"}
    }
    features.append(
        {
            "type": "Feature",
            "properties": properties,
            "geometry": {
                "type": "Point",
                "coordinates": [asset["longitude"], asset["latitude"]],
            },
        }
    )

geojson = {
    "type": "FeatureCollection",
    "name": "infrastructure_assets",
    "features": features,
}

geojson_path = SAMPLE_DIR / "infrastructure_assets.geojson"
geojson_path.write_text(json.dumps(geojson, indent=2), encoding="utf-8")


# -----------------------------------------------------------------------------
# 2. Normal incoming updates
# -----------------------------------------------------------------------------
# AST-999 is intentionally not present in the GIS dataset. It should NOT crash
# the workflow; later we will capture it in an unmatched-record report.
valid_updates = pd.DataFrame(
    [
        ["AST-001", "Active", "High", "L. Nguyen", "2026-09-20"],
        ["AST-003", "Maintenance", "High", "L. Nguyen", "2026-09-21"],
        ["AST-005", "Active", "Medium", "R. Gomez", "2026-09-22"],
        ["AST-007", "Active", "High", "R. Gomez", "2026-09-23"],
        ["AST-999", "Active", "Low", "R. Gomez", "2026-09-24"],
    ],
    columns=[
        "asset_id",
        "status_new",
        "priority_new",
        "inspector_new",
        "inspection_date",
    ],
)


# -----------------------------------------------------------------------------
# 3. Failure-case sheets
# -----------------------------------------------------------------------------
duplicate_id_test = valid_updates.copy()
duplicate_id_test.loc[len(duplicate_id_test)] = [
    "AST-003",
    "Active",
    "Low",
    "Test User",
    "2026-09-25",
]

null_id_test = valid_updates.copy()
null_id_test.loc[len(null_id_test)] = [
    None,
    "Active",
    "Low",
    "Test User",
    "2026-09-25",
]

missing_column_test = valid_updates.drop(columns=["priority_new"])


xlsx_path = SAMPLE_DIR / "incoming_updates.xlsx"
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
    valid_updates.to_excel(writer, sheet_name="updates", index=False)
    duplicate_id_test.to_excel(writer, sheet_name="duplicate_id_test", index=False)
    null_id_test.to_excel(writer, sheet_name="null_id_test", index=False)
    missing_column_test.to_excel(writer, sheet_name="missing_column_test", index=False)


print("Day 01 synthetic data created successfully.")
print(f"GeoJSON: {geojson_path}")
print(f"Excel:   {xlsx_path}")
print(f"GIS assets: {len(assets)}")
print(f"Incoming update rows: {len(valid_updates)}")
print("Expected unmatched ID in normal sheet: AST-999")
