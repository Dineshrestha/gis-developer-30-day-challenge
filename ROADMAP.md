# 30-Day GIS Developer Roadmap

This roadmap is intentionally iterative. Topics may be refined as real job requirements, project ideas, and learning needs emerge.

## Week 1 — Developer Foundations

### Day 01 — Excel → GIS Update Automation
Build a configurable Python/ArcPy/pandas workflow that validates incoming tabular records, matches them to GIS features, updates attributes, and reports unmatched records.

### Day 02 — Production-Quality Python GIS Tool
Refactor a GIS workflow into reusable functions/modules with configuration, logging, exceptions, and portable paths.

### Day 03 — Rule-Based GIS QA/QC Engine
Convert business rules into reusable automated GIS validation checks.

### Day 04 — Testing GIS Code
Use test datasets and assertions to verify schemas, attributes, geometries, expected failures, and regression behavior.

### Day 05 — Batch GIS ETL / Standardization
Ingest mixed datasets, validate schemas, standardize projection/naming, transform data, and write consistent outputs.

### Day 06 — Spatial & Attribute Change Detection
Identify additions, deletions, attribute edits, and geometry changes between versions of a dataset.

### Day 07 — Automation ROI
Benchmark manual vs automated processing and communicate time savings and operational value.

## Week 2 — Spatial Data Engineering & Enterprise GIS

### Day 08 — PostgreSQL/PostGIS
Build a spatial database with schemas, constraints, geometry columns, relationships, and spatial indexes.

### Day 09 — Spatial SQL & Performance
Practice spatial queries such as `ST_Intersects`, `ST_Within`, `ST_Distance`, `ST_Buffer`, and `ST_Transform`, plus query tuning.

### Day 10 — GIS Data Reconciliation
Resolve conflicting records from multiple datasets using explicit authoritative-source rules.

### Day 11 — ArcGIS REST API
Query feature services using REST, authentication, JSON, filters, pagination, and service metadata.

### Day 12 — ArcGIS API for Python
Automate Portal/ArcGIS Online searches, item administration, feature-layer updates, and publishing workflows.

### Day 13 — ArcGIS Services
Understand and work with Feature Services, Map Services, and Geoprocessing Services, including permissions and troubleshooting.

### Day 14 — Enterprise GIS Architecture
Design a conceptual Enterprise GIS system including Portal, ArcGIS Server, databases, authentication, permissions, backup, monitoring, and resilience.

## Week 3 — Modern Web GIS

### Day 15 — JavaScript / TypeScript for GIS Developers
Practice the language features most useful in GIS applications: objects, arrays, functions, async/await, modules, interfaces, types, and API calls.

### Day 16 — Modern Web Tooling
Use Node.js, npm, package.json, Vite, source folders, dependencies, development servers, and production builds.

### Day 17 — React Fundamentals
Build GIS-oriented React components using props, state, hooks, events, and reusable UI structure.

### Day 18 — React + ArcGIS Maps SDK for JavaScript
Integrate an ArcGIS map and feature layers inside a React application.

### Day 19 — GIS Web Application
Build a responsive GIS application with filtering, selection, popups, statistics, and user interaction.

### Day 20 — Authentication & Secure APIs
Understand OAuth, tokens, API keys, CORS, credential handling, role-based access, and least privilege.

### Day 21 — Experience Builder Development
Explore the architecture and workflow behind custom widgets and extend Experience Builder beyond configuration.

## Week 4 — Backend, DevOps & Architecture

### Day 22 — GIS Backend API
Create spatial endpoints using FastAPI.

### Day 23 — Full-Stack Geospatial Workflow
Connect React → REST API → FastAPI → PostGIS and return spatial results to the map.

### Day 24 — Docker
Containerize an open-source geospatial backend and manage environment variables and dependencies.

### Day 25 — CI/CD with GitHub Actions
Automatically test and validate code on pushes and pull requests.

### Day 26 — Cloud GIS Architecture
Map a web GIS architecture to core AWS/Azure services and understand deployment patterns.

### Day 27 — Security, Testing & Performance
Practice unit, integration, API, UAT, and performance testing plus secure configuration and accessibility concepts.

### Day 28 — Advanced Lab: B2H Cultural Site Batch Viewshed & Visibility Automation
Turn a proven single-site viewshed workflow into one production-scale batch geoprocessing system for approximately 90 cultural sites containing point, line, and polygon geometries.

This advanced lab remains **one challenge slot**, even though it is intentionally larger than the standard one-hour exercise. The public portfolio version must reproduce the engineering methodology with public or synthetic substitutes rather than proprietary project data.

The lab will cover the complete system as one integrated workflow:

- reproduce the single-site prototype with a 6-ft observer, terrain viewshed, 5-mile structure search, visibility interpretation, QA, and report generation;
- scale from one observer/site to approximately 90 mixed-geometry sites;
- implement the client-approved **Any Location** rule: a structure is potentially visible when it is visible from at least one observer generated from the full site geometry;
- use a single observer for point sites and multiple observers for line/polygon sites instead of relying on a midpoint or centroid, because one representative location can miss visibility from other portions of a site and understate potential visibility;
- evaluate 10 m versus 30 m DEM resolution, including the accuracy/runtime/storage tradeoff that led to the production-scale 30 m approach;
- acquire DEM coverage for buffered analysis extents, manage multiple source tiles, mosaic them into a continuous analysis surface, and verify coverage before processing;
- use a final 500 m observer spacing for line/polygon sites to balance spatial coverage with practical runtime;
- batch the workflow with ArcPy so each site's observers, 5-mile analysis extent, terrain visibility, and potentially visible Rev2d structures are processed consistently;
- package the workflow as a user-friendly Python Toolbox with clear parameters, sensible defaults, progress messages, and reusable configuration;
- make per-site viewshed-raster export optional so users can preserve diagnostic rasters when needed without forcing large raster outputs for every site;
- generate an automated Excel deliverable containing site-level summaries, visible-structure lists, counts, QA/status information, and batch-run results;
- implement preflight and post-run QA for site IDs, geometry types, projected coordinate system, DEM resolution/coverage, observer generation, structure IDs/heights, duplicate records, failed sites, missing outputs, and processing completeness;
- benchmark the automated system against the original manual workflow.

**Efficiency case study:** the original single-point workflow took about 3 hours. Even if all 90 sites had been simple points, manual production would have required about 270 labor-hours; because line and polygon sites require more observers and processing, the realistic manual estimate is **greater than 270 hours**. The automated production workflow was completed by a two-person team in roughly 8 hours each, or about **16 labor-hours**. Against the conservative 270-hour baseline, that represents at least **254 labor-hours avoided**, approximately **94.1% labor reduction**, and roughly **16.9× greater throughput**. The actual gain is larger when the additional manual complexity of line and polygon sites is considered.

The advanced lab deliverables will include reusable ArcPy modules, a Python Toolbox, configuration, QA/logging, automated Excel reporting, optional raster outputs, benchmark documentation, and a concise architecture/workflow diagram.

### Day 29 — GIS System Design & Requirements
Turn an ambiguous business request into requirements, user stories, acceptance criteria, architecture, API contracts, database design, testing strategy, and sprint work.

### Day 30 — Full-Stack Geospatial Capstone
Build and document an end-to-end geospatial application combining ingestion, QA/QC, spatial processing, database, API, web mapping, testing, CI/CD, and architecture documentation.
