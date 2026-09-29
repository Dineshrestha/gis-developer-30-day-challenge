# Sample Data

Day 01 uses **synthetic data only**.

The source generator is committed at:

`../create_sample_data.py`

Running it creates the local exercise inputs:

- `authoritative_assets.geojson` — 1,000 synthetic authoritative GIS assets
- `xyz_field_delivery.xlsx` — 300 synthetic Client XYZ field records

Those generated files are intentionally ignored by Git. This keeps the repository lightweight while making the exercise fully reproducible from code.

The client workbook includes a `scenario_expected` field and an `Expected_Test_Counts` sheet only for training verification. A real client delivery would not contain an answer key.

Never commit employer/client datasets, internal paths, credentials, proprietary schemas, confidential attributes, or personally identifiable information.
