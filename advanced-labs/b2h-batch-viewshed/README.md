# Advanced Portfolio Lab — B2H Cultural Site Batch Viewshed & Visibility Automation

## Lab Type

**One advanced portfolio lab outside the 30 numbered days.** This project does not replace Day 28 and does not expand into multiple challenge days.

The public portfolio version must reproduce the engineering methodology with public or synthetic replacement data. Do not publish proprietary B2H datasets, internal paths, client identifiers, or restricted project outputs.

## Business Problem

A single-site viewshed and visibility workflow was first developed and validated for one cultural location. That workflow required roughly **3 hours** to prepare inputs, run the terrain analysis, determine which project structures could potentially be seen, perform QA, and prepare the visibility report.

The scope then expanded to approximately **90 cultural sites** represented by a mix of points, lines, and polygons. The required output was a reliable list of Rev2d structures potentially visible from each cultural site.

Running the original one-site process independently for every location was not operationally viable. Ninety simple point sites alone imply approximately **270 labor-hours**, and the actual mixed-geometry scope would require more because line and polygon sites need multiple observers.

The developer problem is therefore to redesign a validated one-off spatial analysis as a configurable, auditable, production-scale batch system.

## Single-Site Foundation

The advanced lab begins by reproducing the validated single-site logic:

1. Use the cultural site as the observer source.
2. Apply a final observer height of **6 ft above ground**.
3. Prepare DEM coverage for the analysis area.
4. Run the terrain viewshed.
5. Evaluate project structures within a **5-mile** search distance.
6. Use structure identifiers and heights in the visibility interpretation.
7. Classify structures as potentially visible or obscured according to the approved logic.
8. QA the input data, DEM, structures, visibility output, and reporting totals.
9. Generate a structured visibility report.

The single-site prototype establishes analytical correctness before any scaling work begins.

## Scaling to ~90 Point / Line / Polygon Sites

### Point Sites

A point naturally provides one observer location.

### Line and Polygon Sites

A midpoint or centroid is not sufficient for a conservative **Any Location** question. A structure hidden from a centroid may still be visible from another portion of the site.

The batch workflow therefore generates **multiple observer points across line and polygon geometry**. A structure is classified as potentially visible from a site when it is visible from **at least one site observer**.

The final production configuration uses approximately **500 m observer spacing** for line and polygon sites to balance spatial coverage against computational runtime.

## DEM Engineering — 10 m vs. 30 m

DEM development is part of the engineering exercise, not a hidden preprocessing step.

The lab should document:

- locating and downloading elevation coverage;
- buffering acquisition/analysis extents so viewsheds are not truncated at DEM edges;
- downloading multiple source tiles when needed;
- mosaicking tiles into a continuous analysis surface;
- verifying coordinate system, cell size, extent, NoData, and coverage;
- testing the higher-detail **10 m DEM** approach;
- measuring runtime/storage as observer counts and site counts increase;
- selecting a **30 m DEM** production approach when 10 m processing becomes impractical at batch scale.

The engineering lesson is that the highest-resolution source is not automatically the best production choice. Resolution must be balanced against analytical purpose, runtime, storage, reproducibility, and delivery constraints.

## Batch Architecture

```text
Cultural Sites
(points / lines / polygons)
        │
        ▼
Preflight QA
        │
        ▼
Standardize IDs + geometry
        │
        ▼
Generate Observers
Point → one observer
Line/Polygon → observers at configured spacing
        │
        ▼
5-mile site analysis extent
        │
        ▼
DEM coverage validation
        │
        ▼
Terrain viewshed processing
        │
        ▼
Evaluate Rev2d structures
        │
        ▼
Visible from ≥1 observer?
        │
   ┌────┴────┐
   ▼         ▼
Visible    Obscured
   │
   ▼
Per-site results
   ├── Automated Excel report
   ├── QA / run log
   └── Optional viewshed raster
```

## ArcPy Batch Processing

Implement the production workflow as reusable ArcPy modules rather than one large procedural script.

The system should:

- discover and validate inputs;
- standardize point, line, and polygon site records;
- generate observer locations;
- manage site-level search extents;
- validate DEM coverage;
- execute terrain visibility processing;
- evaluate Rev2d structures against each site's visibility result;
- collect per-site statistics;
- write structured outputs;
- catch and log site-level failures without terminating the whole batch where possible;
- report progress and runtime.

## Python Toolbox

Package the workflow as a `.pyt` Python Toolbox so another GIS analyst can run it without editing source code.

Parameters should include, as appropriate:

- point cultural sites;
- line cultural sites;
- polygon cultural sites;
- site ID field;
- DEM;
- Rev2d structures;
- structure ID field;
- structure-height field;
- observer height;
- structure search distance;
- observer spacing;
- output workspace;
- Excel report location;
- **Save Viewshed Rasters** option.

Production defaults should reflect the final methodology, including **6 ft observer height**, **5-mile search distance**, and **500 m observer spacing** for line/polygon sites.

## Optional Raster Outputs

Saving every viewshed raster can substantially increase storage and processing overhead.

The toolbox should therefore support:

- **Off** — use temporary/intermediate rasters and retain only tabular/summary results.
- **On** — preserve per-site viewshed rasters for QA, investigation, mapping, or requested documentation.

## Automated Excel Reporting

The batch system should generate the Excel deliverable directly from processing results.

At minimum, include:

- batch summary;
- one row per cultural site;
- geometry type;
- observer count;
- structures evaluated;
- potentially visible structure count;
- potentially visible Rev2d structure IDs;
- run status;
- QA notes/errors;
- processing time where useful;
- a detailed site-to-structure table for review/filtering.

The Excel output and GIS processing results must come from the same structured result objects so they cannot drift apart through manual transcription.

## QA / Validation

Preflight QA should check required inputs, geometry types, non-null/unique site IDs, projected coordinate systems, compatible units, structure IDs/heights, DEM resolution/extent/NoData, DEM coverage, observer generation, expected observer counts, valid geometry, and required ArcGIS analysis capability.

Post-run QA should reconcile all expected sites, successful/failed site counts, failure messages, visible-structure IDs, summary/detail counts, Excel totals, optional raster outputs, and overall processing completeness. No site should be silently omitted.

## Performance Engineering Case Study

Original single-site workflow:

```text
~3 hours/site
```

Conservative manual baseline:

```text
90 sites × 3 hours/site = 270 labor-hours
```

That estimate is intentionally conservative because it treats every site like a simple point. Line and polygon sites require multiple observers and additional processing, so realistic manual effort is **greater than 270 hours**.

Automated production effort:

```text
2 people × ~8 hours = ~16 labor-hours
```

Conservative impact:

```text
Labor-hours avoided = 270 - 16 = 254 hours
Labor reduction      = 254 / 270 ≈ 94.1%
Throughput gain      = 270 / 16 ≈ 16.9×
```

The true gain is larger because the actual manual baseline exceeds 270 hours.

## Key Engineering Decisions to Document

- validate the analytical logic on one site before scaling;
- use multiple observers across line/polygon geometry instead of midpoint/centroid-only representation;
- apply an Any Location visibility rule;
- test 10 m DEM before choosing a practical 30 m production surface;
- acquire and mosaic buffered DEM coverage before batch execution;
- settle on 500 m observer spacing after performance tradeoff testing;
- separate temporary analytical rasters from optional retained outputs;
- automate Excel reporting from the same structured batch results;
- expose the process through a Python Toolbox;
- build QA into the workflow rather than adding it at the end.

## Deliverables

- reusable ArcPy modules/scripts;
- Python Toolbox (`.pyt`);
- public/synthetic point, line, polygon, structure, and DEM test data or documented public sources;
- configuration/default parameters;
- batch run log;
- QA report;
- automated Excel visibility workbook;
- optional site-level viewshed rasters;
- architecture/workflow diagram;
- manual-vs.-automated benchmark;
- README documenting methodology, decisions, limitations, and lessons learned.

## Acceptance Criteria

- [ ] Single-site logic is reproduced and validated before batch execution.
- [ ] Point, line, and polygon sites are supported.
- [ ] Line/polygon sites use multiple observers rather than a single midpoint/centroid.
- [ ] Final configurable observer spacing supports the 500 m methodology.
- [ ] Observer height defaults to 6 ft.
- [ ] Structure search distance defaults to 5 miles from site geometry.
- [ ] A structure is potentially visible when visible from at least one observer.
- [ ] Only the intended Rev2d structure inventory is reported.
- [ ] DEM preparation documents the 10 m vs. 30 m decision.
- [ ] Buffered DEM acquisition and mosaicking are reproducible.
- [ ] Batch processing supports site-level failure logging and continuation.
- [ ] Python Toolbox parameters are understandable without source edits.
- [ ] Viewshed raster retention is optional.
- [ ] Excel reporting is generated automatically.
- [ ] Preflight and post-run QA reconcile all expected sites and outputs.
- [ ] Benchmark documents >270 manual labor-hours versus ~16 automated labor-hours.
- [ ] Public repository contains no proprietary B2H data, internal paths, credentials, or restricted outputs.

## Portfolio / Interview Story

> A validated single-site viewshed workflow took roughly three hours per location. When the scope expanded to about 90 point, line, and polygon cultural sites, I redesigned the methodology as a batch ArcPy system. I replaced centroid-only assumptions with multiple observers across full site geometries, evaluated DEM-resolution and observer-spacing tradeoffs, built buffered DEM mosaics, packaged the workflow as a Python Toolbox, automated Excel reporting and QA, and made raster retention optional. The resulting workflow reduced a conservative 270+ labor-hour manual requirement to roughly 16 labor-hours—at least a 94% reduction—while making the process repeatable and usable by other GIS staff.
