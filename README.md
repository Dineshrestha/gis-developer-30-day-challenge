# 30 Days of GIS Development

A practical, problem-driven journey from GIS analysis toward **GIS development, geospatial automation, spatial data engineering, web GIS, and software engineering**.

Rather than learning tools in isolation, each day begins with a realistic GIS problem and works toward a reusable, testable, documented solution.

## Goals

- Build production-minded GIS automation with Python and ArcPy
- Strengthen spatial data engineering with pandas, GeoPandas, SQL, and PostGIS
- Work with ArcGIS REST APIs and the ArcGIS API for Python
- Build modern web GIS applications with TypeScript, React, and the ArcGIS Maps SDK for JavaScript
- Develop backend APIs with FastAPI
- Practice testing, logging, configuration, Git/GitHub, Docker, CI/CD, and cloud concepts
- Learn to communicate technical work as measurable business and scientific impact

## Developer Workflow

Every exercise follows the same general pattern:

**Problem → Requirements → Data → Architecture → Business Rules → Development → Validation → Testing → Documentation → Impact**

## Progress

**Status key:** 🟢 Complete · 🟡 In progress · ⚪ Planned

| Day | Project | Primary Skills | Status |
|---:|---|---|:---:|
| 01 | Client Field Data Validation & GIS Reconciliation | Python, ArcPy, pandas, QA/QC, Excel dashboard | 🟡 |
| 02 | Production-Quality Python GIS Tool | Python structure, config, logging | ⚪ |
| 03 | Rule-Based GIS QA/QC Engine | Python, GIS validation | ⚪ |
| 04 | GIS Code Testing | pytest, test data, assertions | ⚪ |
| 05 | Batch GIS ETL / Standardization | ArcPy, ETL, schemas | ⚪ |
| 06 | Change Detection | pandas, GeoPandas, geometry comparison | ⚪ |
| 07 | Automation ROI | benchmarking, reporting | ⚪ |
| 08 | PostgreSQL / PostGIS | spatial database design | ⚪ |
| 09 | Spatial SQL & Performance | PostGIS, indexes, query tuning | ⚪ |
| 10 | Data Reconciliation | authoritative-source rules | ⚪ |
| 11 | ArcGIS REST API | REST, JSON, pagination | ⚪ |
| 12 | ArcGIS API for Python | Portal, feature layers, publishing | ⚪ |
| 13 | ArcGIS Services | Feature/Map/GP services | ⚪ |
| 14 | Enterprise GIS Architecture | Portal, Server, databases, security | ⚪ |
| 15 | JavaScript / TypeScript for GIS | TS, async/await, modules | ⚪ |
| 16 | Modern Web Tooling | Node.js, npm, Vite | ⚪ |
| 17 | React Fundamentals | components, state, hooks | ⚪ |
| 18 | React + ArcGIS Maps SDK | web mapping | ⚪ |
| 19 | GIS Web Application | filters, selection, statistics | ⚪ |
| 20 | Authentication & Secure APIs | OAuth, tokens, RBAC | ⚪ |
| 21 | Experience Builder Development | custom widget concepts | ⚪ |
| 22 | GIS Backend API | FastAPI, spatial backend | ⚪ |
| 23 | Full-Stack Geospatial Workflow | React, FastAPI, PostGIS | ⚪ |
| 24 | Docker | containers, environment variables | ⚪ |
| 25 | CI/CD | GitHub Actions, automated tests | ⚪ |
| 26 | Cloud GIS Architecture | AWS/Azure concepts | ⚪ |
| 27 | Security, Testing & Performance | integration/UAT/performance | ⚪ |
| 28 | GIS Engineering Experiment | raster methodology, validation | ⚪ |
| 29 | GIS System Design | requirements, architecture, Agile | ⚪ |
| 30 | Full-Stack Geospatial Capstone | end-to-end integration | ⚪ |

## Daily Structure

Each tutorial is designed for approximately **1 hour**:

- **5 min** — Understand the problem
- **10 min** — Define requirements and approach
- **10 min** — Inspect the data
- **20 min** — Build the solution
- **5 min** — Test and validate
- **5 min** — Update documentation and commit
- **5 min** — Practice explaining the work

## Repository Principles

1. **No proprietary client or employer data.**
2. Use public or synthetic datasets that make every exercise reproducible.
3. Prefer relative paths and configuration over machine-specific absolute paths.
4. Separate exploratory notebooks from reusable production code.
5. Treat testing, validation, logging, and documentation as part of the solution.
6. Define acceptance criteria before coding.
7. When the acceptance criteria are met, mark the version complete. New ideas become enhancements rather than moving the original finish line.

## Repository Structure

```text
gis-developer-30-day-lab/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── day-01-excel-gis-update/
│   ├── README.md
│   ├── Day01_Excel_to_GIS_Update_Automation.ipynb
│   ├── config/
│   ├── src/
│   ├── data/sample/
│   ├── output/
│   └── screenshots/
├── docs/
├── assets/
├── README.md
├── ROADMAP.md
└── .gitignore
```

Additional day folders are added as the tutorials are completed.

## License

A license will be selected before public release. Until then, the repository is a personal learning project.
