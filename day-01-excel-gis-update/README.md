# Day 01 — Excel → GIS Update Automation

## Status

⬜ Not started

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

Use only public or synthetic data. The sample dataset will be created as part of the tutorial so the project is reproducible and safe to publish.

## Acceptance Criteria

The final criteria are defined in the Day 01 GitHub Issue before development begins.
