# Day 01 — Excel → GIS Update Automation

## Status

🚧 In progress

## Problem

A GIS team receives recurring Excel records that must be matched to existing GIS features. The current workflow requires manual joins, field updates, review of unmatched records, and repetitive QA.

## Objective

Build a reusable workflow that:

- reads an Excel file,
- validates required columns,
- checks for duplicate and null IDs,
- matches incoming records to GIS features,
- updates selected attributes,
- reports unmatched or invalid records,
- and produces a clear processing summary.

## Developer Focus

This exercise is not only about ArcPy syntax. It introduces:

- defining requirements before coding,
- separating validation from processing,
- reusable functions,
- configurable field mappings,
- logging/reporting,
- testing edge cases,
- GitHub Issues and acceptance criteria.

## Planned Structure

```text
day-01-excel-gis-update/
├── README.md
├── notebook.ipynb
├── src/
│   └── update_features.py
├── data/
│   └── sample/
├── output/
└── screenshots/
```

## Data

Use only public or synthetic data. The sample dataset is generated from code so the project is reproducible and safe to publish.

The repository stores the GIS sample as GeoJSON because it is lightweight and portable. In ArcGIS Pro, convert the GeoJSON to a local feature class before editing or inspection if Add Data does not accept the file directly.

### ArcGIS Pro preparation

Use **JSON To Features**:

- Input JSON or GeoJSON: `data/sample/infrastructure_assets.geojson`
- Output feature class: a local file geodatabase feature class such as `infrastructure_assets`
- Geometry type: `POINT`

This preserves a portable source file in GitHub while using a native geodatabase feature class for ArcPy updates.

## Acceptance Criteria

The final criteria are defined in the Day 01 GitHub Issue before development begins.
