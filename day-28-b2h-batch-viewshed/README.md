# Day 28 — Advanced Lab: B2H Cultural Site Batch Viewshed & Visibility Automation

## Lab Type

**One advanced lab.** This project is intentionally larger than the normal one-hour daily exercise, but it occupies only one slot in the 30-Day GIS Developer Challenge.

The public challenge version reproduces the engineering methodology with public or synthetic replacement data. Do not publish proprietary B2H datasets, internal paths, client identifiers, or restricted deliverables.

## Business Problem

A single-site viewshed and visibility workflow was initially developed and validated for one cultural location. That workflow required roughly **3 hours** to prepare inputs, run the terrain analysis, determine which project structures could potentially be seen, perform QA, and prepare the visibility report.

The scope then expanded to approximately **90 cultural sites** represented by a mix of points, lines, and polygons. The required output was a reliable list of Rev2d structures potentially visible from each cultural site.

Running the original single-site workflow independently for every site was not operationally viable. Ninety simple point sites alone would require approximately 270 labor-hours, and line/polygon sites would take longer because they require multiple observer locations.

The developer problem is therefore not simply to run a viewshed. It is to redesign a validated one-off analysis as a configurable, auditable, production-scale batch system.

## Single-Site Prototype

The original workflow established the analytical foundation:

1. Use the cultural-site location as the observer source.
2. Apply a final observer height of **6 ft above ground**.
3. Prepare DEM coverage for the analysis area.
4. Run a terrain viewshed.
5. Evaluate project structures within a **5-mile** search distance.
6. Use structure identifiers and heights to support the visibility interpretation.
7. Classify structures as potentially visible or obscured according to the approved visibility logic.
8. Perform QA on inputs, terrain coverage, structure attributes, analysis outputs, and report totals.
9. Generate a structured visibility report.

The single-site prototype proved that the visibility logic worked. The scaling problem required a different software architecture.

## Scaling to ~90 Mixed-Geometry Sites

The cultural-site inventory contains point, line, and polygon features.

### Point Sites

A point naturally represents one observer location.

### Line and Polygon Sites

A midpoint or centroid is not sufficient for a conservative **Any Location** visibility question. A structure hidden from a centroid may still be visible from another part of the cultural site.

The batch workflow therefore generates **multiple observer points** from the actual line or polygon geometry. A structure is considered potentially visible from a site when it is visible from **at least one generated observer**.

This preserves the client-approved interpretation:

> Evaluate whether a Rev2d structure could be visible from any location represented across the cultural-site geometry, rather than from only one arbitrary representative point.

The final production configuration uses approximately **500 m observer spacing** for line and polygon sites, balancing coverage and computational runtime.

## DEM Engineering: 10 m → 30 m

DEM preparation became a major part of the engineering work.

The development process included:

- locating suitable elevation coverage,
- downloading source DEM tiles,
- expanding acquisition around buffered project/site extents so viewshed calculations were not truncated at tile boundaries,
- mosaicking multiple DEM tiles into a continuous analysis raster,
- verifying coordinate system, cell size, extent, NoData, and coverage,
- testing the higher-detail **10 m DEM** approach,
- evaluating runtime and storage as the workflow scaled to many sites and many observers,
- and moving to a **30 m DEM** production approach when the 10 m workflow proved too computationally expensive for the batch requirement.

This is a core engineering lesson of the lab: the most detailed dataset is not automatically the best production dataset. Resolution must be evaluated against analytical purpose, runtime, storage, reproducibility, and delivery deadlines.

## Batch Processing Architecture

```text
Cultural Sites
(points / lines / polygons)
        │
        ▼
Preflight QA
        │
        ▼
Standardize site IDs + geometry
        │
        ▼
Generate observers
Point → 1 observer
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
        │
        ├── Excel reporting
        ├── QA / run log
        └── Optional viewshed raster
```

## ArcPy Automation

The production workflow should be implemented as reusable ArcPy code rather than one large procedural notebook/script.

Recommended responsibilities:

- discover and validate inputs;
- standardize point/line/polygon site records;
- generate observer locations;
- manage site-level search areas;
- validate DEM coverage;
- execute terrain visibility processing;
- evaluate Rev2d structures against site visibility;
- collect per-site statistics;
- write structured outputs;
- catch and log site-level failures without terminating the entire batch;
- report progress and runtime.

A failed site should be recorded for investigation while the remaining sites continue processing whenever possible.

## Python Toolbox

Package the finished workflow as a `.pyt` Python Toolbox so another GIS analyst can use it without editing Python source code.

The toolbox should expose clear parameters for items such as:

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

Use sensible defaults for the final methodology, including **6 ft observer height**, **5-mile search distance**, and **500 m line/polygon observer spacing**.

## Optional Raster Outputs

Saving every site-level viewshed raster can substantially increase storage and processing overhead.

The toolbox therefore makes raster persistence optional:

- **Off** — use temporary/intermediate rasters only and retain the tabular visibility results.
- **On** — preserve site-level viewshed rasters for QA, investigation, mapping, or client-requested documentation.

This separates analytical processing requirements from archival-output requirements.

## Automated Excel Reporting

Generate the batch report automatically rather than manually compiling results after geoprocessing.

The workbook should include at minimum:

- a batch summary;
- one row per cultural site;
- geometry type;
- observer count;
- structures evaluated;
- potentially visible structure count;
- potentially visible Rev2d structure IDs;
- run status;
- QA notes/errors;
- processing time where useful;
- a detailed site-to-structure table suitable for filtering and review.

The reporting layer should be generated directly from the same structured results used by the batch processor so the GIS outputs and Excel totals cannot drift apart through manual transcription.

## QA / Validation

Preflight QA should verify:

- all required inputs exist;
- supported point, line, and polygon geometry types;
- stable/non-null site IDs;
- duplicate site IDs;
- valid projected coordinate system and compatible units;
- valid structure IDs and structure-height values;
- DEM coordinate system, resolution, extent, and usable elevation range;
- complete DEM coverage for each required analysis area;
- observer generation and spacing;
- expected observer counts;
- valid site geometries;
- required ArcGIS analysis capability/license availability.

Post-run QA should verify:

- every expected site was attempted;
- successful/failed site counts reconcile to total inputs;
- failed sites have diagnostic messages;
- structure lists contain valid IDs only;
- visible counts reconcile with detailed tables;
- Excel totals reconcile with processing results;
- optional rasters exist only when requested;
- no site was silently omitted.

## Performance Engineering Case Study

The original single-site workflow required approximately **3 hours**.

Conservative manual baseline:

```text
90 sites × 3 hours/site = 270 labor-hours
```

That baseline is already optimistic because it assumes every site behaves like a simple point. Line and polygon sites require multiple observers and therefore more processing.

The automated workflow made the production task achievable in approximately:

```text
2 people × 8 hours = 16 labor-hours
```

Using 270 hours as the conservative baseline:

```text
Labor-hours avoided = 270 - 16 = 254 hours
Labor reduction      = 254 / 270 ≈ 94.1%
Throughput gain      = 270 / 16 ≈ 16.9×
```

Because the realistic manual requirement was **greater than 270 hours**, the actual efficiency gain is greater than these conservative figures.

## Key Engineering Decisions

This lab should explicitly document the decisions, failed approaches, and tradeoffs—not only the final code:

- prove the analytical logic on one site before scaling;
- represent line/polygon sites with multiple observers instead of one midpoint/centroid;
- use an Any Location visibility rule;
- experiment with 10 m elevation data before selecting a practical 30 m production surface;
- download DEM coverage beyond the immediate site footprint and mosaic tiles before batch execution;
- reduce observer density to a final 500 m production spacing after runtime testing;
- separate temporary analysis rasters from optional retained outputs;
- centralize reporting rather than manually compiling per-site results;
- expose the workflow through a Python Toolbox so it is usable by staff who did not write the code;
- build QA into the workflow rather than treating QA as a final manual step.

## Deliverables

The advanced lab should finish with:

- reusable ArcPy modules/scripts;
- Python Toolbox (`.pyt`);
- synthetic/public point, line, polygon, structure, and DEM test data or documented public sources;
- configuration/default parameters;
- batch processing log;
- QA report;
- automated Excel visibility workbook;
- optional site-level viewshed rasters;
- workflow/architecture diagram;
- benchmark showing manual-versus-automated labor impact;
- README documenting methodology, design decisions, limitations, and lessons learned.

## Acceptance Criteria

- [ ] Single-site logic is reproduced and validated before batch execution.
- [ ] Point, line, and polygon cultural-site geometries are supported.
- [ ] Line/polygon sites use multiple observers rather than a single midpoint/centroid.
- [ ] Final configurable observer spacing supports the 500 m production methodology.
- [ ] Observer height defaults to 6 ft.
- [ ] Structure search distance defaults to 5 miles from the site geometry.
- [ ] A structure is classified as potentially visible when visible from at least one site observer.
- [ ] Only the intended Rev2d structure inventory is reported.
- [ ] DEM preparation documents the 10 m versus 30 m engineering decision.
- [ ] Buffered DEM acquisition and mosaicking are reproducible.
- [ ] Batch processing continues across sites with site-level error logging.
- [ ] Python Toolbox parameters are understandable without modifying source code.
- [ ] Viewshed-raster persistence is optional.
- [ ] Excel reporting is generated automatically from batch results.
- [ ] Preflight and post-run QA reconcile all expected sites and outputs.
- [ ] Benchmark documentation includes the >270-hour manual estimate versus ~16 labor-hours automated.
- [ ] Public repository contains no proprietary B2H data, internal paths, credentials, or restricted project outputs.

## Portfolio / Interview Story

> A validated single-site viewshed workflow took roughly three hours per location. When the scope expanded to about 90 point, line, and polygon cultural sites, I redesigned the methodology as a batch ArcPy system. I replaced centroid-only assumptions with multiple observers across full site geometries, evaluated DEM-resolution and observer-spacing tradeoffs, built buffered DEM mosaics, packaged the workflow as a Python Toolbox, automated Excel reporting and QA, and made raster retention optional. The resulting workflow reduced a conservative 270+ labor-hour manual requirement to roughly 16 labor-hours—at least a 94% reduction—while making the process repeatable and usable by other GIS staff.
