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

### Day 28 — GIS Engineering Experiment
Formalize a real spatial methodology question into hypotheses, automated scenarios, measurable validation, and a defensible recommendation.

This lab is about **methodology engineering**, not merely running geoprocessing tools. The workflow should follow:

**Question → Hypothesis → Scenarios → Automated Testing → Quantitative/Visual Validation → Recommendation**

A representative exercise is the agricultural-mask / tree-canopy boundary problem: compare alternatives such as baseline geometry, inward-buffer scenarios, raster-cell shrink, or other boundary refinements; measure the impact on tree canopy and other land-cover classes; inspect geometry/edge behavior; document tradeoffs; and select a method based on evidence rather than preference.

Core skills include experimental design, scenario automation, sensitivity analysis, raster/vector comparison, metric design, visual QA, reproducibility, and technical decision documentation.

### Day 29 — GIS System Design & Requirements
Turn an ambiguous business request into requirements, user stories, acceptance criteria, architecture, API contracts, database design, testing strategy, and sprint work.

### Day 30 — Full-Stack Geospatial Capstone
Build and document an end-to-end geospatial application combining ingestion, QA/QC, spatial processing, database, API, web mapping, testing, CI/CD, and architecture documentation.

## Advanced Portfolio Lab — B2H Cultural Site Batch Viewshed & Visibility Automation

This is **one advanced lab outside the 30 numbered days**. It does not replace Day 28 or expand into multiple challenge days.

Turn a proven single-site viewshed workflow into one production-scale batch geoprocessing system for approximately 90 cultural sites containing point, line, and polygon geometries.

The integrated lab covers:

- the original single-site workflow with a 6-ft observer, terrain viewshed, 5-mile structure search, QA, and visibility reporting;
- scaling to ~90 mixed-geometry sites;
- the client-approved **Any Location** methodology, with multiple observers for line/polygon features instead of midpoint/centroid-only representation;
- 10 m versus 30 m DEM development and the accuracy/runtime/storage tradeoff;
- buffered DEM acquisition, tile management, mosaicking, and coverage QA;
- final 500 m observer spacing for line/polygon sites;
- ArcPy batch processing and site-level error handling;
- a reusable Python Toolbox with sensible defaults and clear parameters;
- optional per-site viewshed-raster retention;
- automated Excel visibility reporting;
- preflight and post-run QA;
- performance benchmarking and documentation.

**Efficiency case study:** the original single-point workflow took about 3 hours. Ninety simple point sites would therefore require about 270 labor-hours, while the real mixed-geometry scope would exceed that. The automated production workflow required roughly 16 labor-hours total across two people, avoiding at least 254 labor-hours, reducing labor by approximately 94.1%, and yielding roughly 16.9× the conservative manual throughput.

The public portfolio implementation must use public/synthetic replacement data and must not expose proprietary B2H datasets, internal paths, client identifiers, or restricted outputs.

Full advanced-lab specification: `advanced-labs/b2h-batch-viewshed/README.md`
