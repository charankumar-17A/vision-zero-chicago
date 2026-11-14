# Vision Zero Chicago
## Automated Safety Capital Investment Prioritization System

**Data Analytics Capstone Project**

---

| | |
|---|---|
| **Prepared by** | B. Charan Kumar |
| **Mentor** | Nithyasri |
| **Program** | Data Analytics G1 |
| **Organization** | SURE Trust (Skill Upgradation for Rural-youth Empowerment Trust) |
| **Submission Date** | September 2026 |
| **Live Dashboard** | [vision-zero-chicago-charan.streamlit.app](https://vision-zero-chicago-charan.streamlit.app/) |
| **GitHub Repository** | [CharanKumar17-a/vision-zero-chicago](https://github.com/CharanKumar17-a/vision-zero-chicago) |

---

> *A data-driven decision-support system for prioritizing corridor-level road-safety investments
> under budget and equity constraints, aligned with the City of Chicago's Vision Zero initiative.*
>
> *The system supports decisions. It does not automatically approve projects. Final project
> selection authority remains with City staff and qualified transportation-engineering teams.*

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Project Objectives](#4-project-objectives)
5. [Project Scope and Boundaries](#5-project-scope-and-boundaries)
6. [Data Sources and Collection](#6-data-sources-and-collection)
7. [Data Preparation and Quality Management](#7-data-preparation-and-quality-management)
8. [Spatial Corridor Construction and Crash Assignment](#8-spatial-corridor-construction-and-crash-assignment)
9. [Exploratory Data Analysis](#9-exploratory-data-analysis)
10. [Equity Analysis](#10-equity-analysis)
11. [Forecasting Methodology](#11-forecasting-methodology)
12. [Empirical Bayes Stabilization](#12-empirical-bayes-stabilization)
13. [Treatment Applicability](#13-treatment-applicability)
14. [Crash Modification Factors](#14-crash-modification-factors)
15. [Benefit-Cost Analysis](#15-benefit-cost-analysis)
16. [Portfolio Optimization](#16-portfolio-optimization)
17. [System Architecture](#17-system-architecture)
18. [Technology and Tools](#18-technology-and-tools)
19. [Streamlit Application](#19-streamlit-application)
20. [Power BI Dashboard](#20-power-bi-dashboard)
21. [n8n Automation](#21-n8n-automation)
22. [Testing and Quality Assurance](#22-testing-and-quality-assurance)
23. [Results and Findings](#23-results-and-findings)
24. [Social and Industry Relevance](#24-social-and-industry-relevance)
25. [Limitations and Responsible Use](#25-limitations-and-responsible-use)
26. [Learning and Reflection](#26-learning-and-reflection)
27. [Future Scope](#27-future-scope)
28. [Conclusion](#28-conclusion)
29. [GitHub and Project Resources](#29-github-and-project-resources)
30. [References](#30-references)
31. [Appendices](#31-appendices)

---

## 1. Executive Summary

Vision Zero Chicago is a data analytics decision-support system designed to help prioritize
road-safety capital investments across Chicago's 43 designated High-Crash Corridors (HCCs).

The system addresses a constrained capital allocation problem: which combination of corridor-level
safety treatment projects maximizes expected societal safety benefit under a limited planning budget
and an equity-spending requirement?

Rather than simply ranking corridors by historical crash counts, the system evaluates 129
corridor-treatment project candidates through a connected five-layer pipeline:

1. **Data and spatial processing** -- 877,919 cleaned police-reported crash records spatially
   assigned to corridors using a governed 100-foot matching rule
2. **Crash-risk forecasting** -- rolling-origin chronological validation, zero future leakage
3. **Empirical Bayes stabilization** -- corrects composition estimates on low-volume corridors
4. **Benefit-cost analysis** -- FHWA-sourced Crash Modification Factors, USDOT 2024 crash costs,
   20-year present-value lifecycle calculation
5. **Mixed-Integer Linear Programming (MILP) portfolio optimization** -- scipy/HiGHS solver,
   globally optimal solutions across 192 scenarios

### Key Verified Results (All Sourced From Validated Pipeline Outputs)

| Metric | Verified Value | Source |
|---|---|---|
| Crash records analyzed | 877,919 (2018-2025) | crash_corridor_assignment_validation.json |
| High-Crash Corridors evaluated | 43 | corridor_register_validation.json |
| Corridor-assigned crashes | 112,421 | panel validation |
| KSI crashes in corridors | 2,297 (139 fatal + 2,158 serious) | panel validation |
| 2026 total crash forecast | 14,029.8 (43 corridors) | forecast validation |
| Treatment benefit scenarios | 387 | treatment_benefits_validation.json |
| Portfolio scenarios optimized | 192 (27 official + 9 stress + 156 grid) | portfolio validation |
| $15M baseline PV safety benefit | $4.00B | solver_audit.md |
| $15M baseline BCR | 267:1 | solver_audit.md |
| $15M annual KSI crashes avoided | 48.04 | solver_audit.md |
| Critical quality failures | 0 | all validation JSONs |
| Automated acceptance tests | 327 | tests/ directory |

### Responsible Use Statement

The final system is a planning tool for engineering review. It does not make final funding
decisions, replace engineering judgment, establish causal treatment effects in Chicago,
constitute official City policy, or provide real-time crash predictions.

---

## 2. Introduction

### Vision Zero

Vision Zero is a traffic-safety philosophy originating in Sweden (1997), premised on the position
that traffic fatalities and serious injuries are preventable through systemic road design. The core
commitment: no loss of life or serious injury on public roads is acceptable. By 2026, over 40 U.S.
cities have formally adopted Vision Zero action plans.

### Chicago Road-Safety Context

Chicago's Vision Zero Chicago Action Plan identifies High-Crash Corridors as the primary focus for
infrastructure investment. The 2018 High-Crash Corridor Framework Plan documented 43 corridors
across Chicago's community areas.

Between 2018 and 2025, 139 fatal crashes and 2,158 serious-injury crashes were recorded within
the 43-corridor network -- 2,297 KSI (Killed or Seriously Injured) crashes in total.

### Why Crash Ranking Alone Is Insufficient

A simple corridor ranking does not account for crash severity, future expected burden, treatment
effectiveness, treatment cost, equity requirements, or interaction between projects. The City needs
to know which combination of projects produces the greatest total benefit within its budget.

---

## 3. Problem Statement

### Formal Problem Definition

> Which combination of corridor-treatment projects should be selected to maximize expected total
> present-value societal safety benefit across Chicago's 43 High-Crash Corridors, subject to a
> planning budget ceiling, an equity-spending floor, one treatment per corridor, and treatment
> applicability requirements?

This is a **constrained capital allocation problem** -- specifically a Mixed-Integer Linear
Programming problem -- not a ranking problem.

### Decision Unit

A **corridor-treatment project**: one safety treatment applied to one named High-Crash Corridor.
43 corridors x 3 active treatments = up to 129 candidate projects. The optimizer selects the
feasible subset that maximizes total present-value benefit.

---

## 4. Project Objectives

### Primary Objective

Build a reproducible, governed analytical system that identifies the highest-benefit feasible
combination of corridor-treatment projects under defined budget and equity constraints, producing
a transparent shortlist for City and engineering review.

### Supporting Objectives (All Verified)

1. Establish the 43-corridor candidate network from the 2018 HCC Plan
2. Spatially assign recorded crashes uniquely to corridors (zero double-counting)
3. Construct a balanced 43 x 96 corridor-month historical panel (4,128 rows)
4. Forecast 2026 corridor-level crash burden (rolling-origin protocol)
5. Stabilize sparse KSI crash composition via Empirical Bayes shrinkage
6. Identify treatment-applicable crash populations per corridor
7. Estimate expected annual crashes averted using documented CMFs
8. Monetize safety benefits using USDOT 2024 crash cost guidance
9. Calculate 20-year lifecycle present-value benefit and BCR
10. Optimize project selection via MILP under budget and equity constraints
11. Provide scenario analysis (27 official + 9 stress + 156 grid scenarios)
12. Deliver results through Streamlit scenario planner and Power BI dashboard
13. Automate quality-gated delivery through n8n
14. Maintain reproducibility through validated pipeline stages and 327 acceptance tests

---

## 5. Project Scope and Boundaries

### Included

- 43 official High-Crash Corridors (2018 HCC Plan)
- January 2018 - December 2025 crash history (96 months)
- 2026 planning-year forecast
- 3 active treatments (TRT_001 Refuge Island, TRT_002 Road Diet, TRT_004 RRFB)
- Equity constraint (SVI-based, denominator = total selected spending)
- MILP portfolio optimization across 192 scenarios
- Streamlit scenario planner, Power BI dashboard, n8n delivery automation
- 327-test automated acceptance test suite

### Excluded

- Individual driver risk prediction or enforcement recommendations
- Automatic funding authorization or engineering design approval
- Causal proof of treatment effectiveness in Chicago
- Real-time crash prediction
- Community preference modelling
- Corridors outside the 2018 HCC Plan

**The system output is a planning shortlist, not funding authorization or engineering approval.**

---

## 6. Data Sources and Collection

All data is open and publicly available. No proprietary or personally identifiable data used.
All sources accessed 2026-08-04 through 2026-08-09.

| Source | Provider | Grain | Rows | Primary Use | Key Risk |
|---|---|---|---|---|---|
| Traffic Crashes - Crashes (SRC001) | Chicago Data Portal | One row/crash | 1,080,723 | Crash dates, severity, location | Records may be amended |
| Traffic Crashes - Vehicles (SRC002) | Chicago Data Portal | One row/unit | 2,203,490 | Vehicle mode flags | Multiple units per crash -- must aggregate |
| Traffic Crashes - People (SRC007) | Chicago Data Portal | One row/person | 2,372,047 | Injury classification | Multiple persons per crash -- must aggregate |
| Street Center Lines (SRC008) | Chicago Data Portal | One row/segment | 56,338 | Corridor geometry | 2 empty geometries; must reconstruct |
| 2018 HCC Framework Plan (SRC003) | City of Chicago | One corridor | 43 | Candidate corridor definitions | Historical scope |
| CDC/ATSDR SVI 2022 (SRC004) | CDC/ATSDR | Census tract | -- | Equity area designation | Threshold sensitivity |
| FHWA CMF Clearinghouse (SRC005) | FHWA | Study/treatment | -- | Treatment effectiveness | External validity |
| FHWA STEP Planning Costs (SRC006) | USDOT | Treatment type | -- | Capital cost scenarios | Planning estimates only |

### Vehicle-to-Crash Aggregation

Each crash may have multiple vehicle/unit records. Joining vehicle rows directly to crash outcomes
without prior aggregation inflates crash counts. Vehicle rows are aggregated to crash-level flags
before joining (Decision D002). This is a critical data quality step verified in the cleaning
contract and test suite.

---

## 7. Data Preparation and Quality Management

### Crash Record Processing

| Step | Action | Verified Outcome |
|---|---|---|
| Date filtering | Retain complete months Jan 2018 - Dec 2025 | 8 partial months excluded |
| Severity mapping | Map police injury classification to KABCO | Zero unknown mappings |
| Coordinate validation | Flag records without valid lat/lon | 7,150 flagged (0.81%), preserved |
| Duplicate detection | Verify crash record ID uniqueness | 0 duplicates |
| Vehicle aggregation | Aggregate vehicle rows to crash-level before joining | Inflation prevented |

### Data Quality Check Results (From Validated Pipeline Outputs)

| Check | Expected | Actual | Status |
|---|---|---|---|
| Duplicate crash record IDs | 0 | 0 | PASS |
| Crashes without valid dates | 0 | 0 | PASS |
| Invalid coordinates (preserved in raw totals) | -- | 7,150 | PRESERVED |
| Vehicle join count inflation | 0 | 0 | PASS |
| Unknown KABCO severity values | 0 | 0 | PASS |
| Severity reconciliation diff (K+A+B+C+O+U = total) | 0 | 0 | PASS |

---

## 8. Spatial Corridor Construction and Crash Assignment

### Why This Is Non-Trivial

A spatial join can execute successfully while producing incorrect results. Key failure modes:

- Assigning crashes to a nearby parallel road rather than the named corridor
- Assigning one crash to multiple corridors (double-counting)
- Measuring distance in latitude/longitude degrees (systematic error)
- Extending corridors beyond their published boundaries
- Silently excluding crashes without coordinates

These errors corrupt corridor crash counts, forecasts, treatment benefits, and the portfolio.
The spatial methodology is governed by a formal 622-line Spatial Assignment Contract.

### Methodology

1. **CRS reprojection:** All coordinates reprojected from EPSG:4326 to EPSG:3435
   (Illinois State Plane East, feet) via pyproj. This is mandatory -- distance cannot be
   computed from latitude/longitude degrees.

2. **Corridor geometry:** Constructed from Chicago Street Center Lines using endpoint matching
   and segment stitching. Linework coverage: 100.0% across all 43 corridors.

3. **R-Tree spatial index:** STRtree index for high-performance point-to-line queries across
   870,769 geocoded crashes.

4. **100-foot primary assignment rule (Decision D017):** A crash is assigned to the nearest
   corridor within 100.0 feet. Ties within 10 feet flagged as unresolved.

5. **Unique assignment:** Each crash receives at most one primary corridor assignment.

### Assignment Results

| Category | Count | Share |
|---|---|---|
| Primary assigned | 112,421 | 13.12% |
| Unresolved multi-corridor tie | 1,803 | 0.21% |
| Outside 100-ft buffer | 756,545 | 86.88% |
| No valid coordinates (preserved) | 7,150 | 0.81% |
| **Total (reconciliation diff = 0)** | **877,919** | **100.00%** |

### Buffer Sensitivity Analysis

| Threshold | Assigned | Spearman Rank Corr. | $15M Portfolio Overlap |
|---|---|---|---|
| 50 ft | 103,102 | 0.978 | 97% (38/39 corridors) |
| **100 ft (production)** | **112,421** | **1.000** | **100%** |
| 150 ft | 120,171 | 0.988 | 43/43 corridors |

The 100-ft threshold is robust. Corridor prioritization rankings are stable across all three
buffer sizes (Spearman >= 0.978).

---

## 9. Exploratory Data Analysis

*EDA charts are generated by project notebooks (01_crash_eda, 02_corridor_profiles,
04_spatial_analysis). Screenshots of final outputs will be inserted in the print version.*

### Key EDA Findings (Verified From Pipeline Outputs)

**Severity distribution within corridors (2018-2025):**

| Severity Class | Count | Share |
|---|---|---|
| K -- Fatal | 139 | 0.12% |
| A -- Serious Injury | 2,158 | 1.92% |
| B -- Minor Injury | 10,850 | 9.65% |
| C -- Possible Injury | 6,124 | 5.45% |
| O -- Property Damage Only | 93,053 | 82.78% |
| U -- Unknown | 97 | 0.09% |
| **Total** | **112,421** | **100.00%** |

**KSI concentration:** 2,297 KSI crashes = 2.04% of corridor crashes. Despite rarity, KSI
crashes carry the highest unit societal costs and drive most of the present-value benefit.

**Zero-crash months:** 7 of 4,128 corridor-months (0.17%) -- corridors are consistently
high-burden rather than sporadically elevated.

---

## 10. Equity Analysis

### Methodology

**Source:** CDC/ATSDR Social Vulnerability Index 2022, Illinois census tracts.

**Classification:**

| Class | Rule | Count |
|---|---|---|
| Class A (Highest Priority) | Length-weighted mean SVI >= 0.75 | **18** of 43 corridors |
| Class B (High Priority) | >= 50% of corridor length in high-SVI tracts | **19** of 43 corridors |
| Other | Below both thresholds | 6 of 43 corridors |

Sensitivity tested at 40% and 60% overlap thresholds. Results in threshold_sensitivity_report.json.

### Equity Constraint in Optimization

    Equity capital spending / Total selected capital spending >= Equity floor %

The denominator is total **selected** spending, not the available budget ceiling. This ensures
the constraint reflects actual allocation rather than an unspent budget share.

### Achieved Equity

Under all official planning scenarios, the unconstrained optimal selection naturally achieves
**45.18% equity spending share** -- exceeding all equity floors (20%, 30%, 40%) without the
constraint altering project selection. All equity constraints are non-binding under current
unit-cost assumptions.

---

## 11. Forecasting Methodology

### Why Forecasting, Not Historical Counts?

Historical crash counts reflect past burden. Forecasting 2026 expected crash burden provides
a forward-looking basis for estimating crashes a treatment would avert -- which determines benefit.

### Validation Protocol -- Rolling-Origin (No Random Split)

Random train-test splits are prohibited. A random split allows future months into the training set,
producing leak-contaminated performance metrics.

| Split | Period | Corridor-Month Rows |
|---|---|---|
| Warm-up / lag initialization | 2018 | 516 |
| Training | 2019-2023 | 2,580 |
| Validation (model selection) | 2024 | 516 |
| Test / backtest (hindsight) | 2025 | 516 |
| Production forecast | 2026 (12 months) | 516 predictions |

No 2026 data was used in model selection or calibration.

### Model Selection Results

| Target | Selected Model | Val MAE | Val Deviance | Val Calibration |
|---|---|---|---|---|
| Total crashes | **12-Month Rolling Mean** | 5.22 | 1.648 | 0.984 |
| KSI crashes | **Negative Binomial GLM + EB** | 0.595 | 0.988 | 1.000 (post-EB) |

**Total crash rationale:** The 12-Month Rolling Mean outperformed all parameterized GLM and ML
models on validation Poisson deviance and MAE. Reported transparently as an empirical benchmark.

**KSI crash rationale:** KSI exhibits severe zero-inflation (61.6% zero-months) and overdispersion.
NB GLM achieves lowest validation deviance. EB shrinkage corrects the 25.84% overpredict bias.

### 2026 Production Forecast

| Metric | Value |
|---|---|
| Forecast origin | 2025-12-01 |
| Protocol | Fixed-origin recursive with calibrated prediction feedback |
| Total crash forecast (43 corridors) | 14,029.8 |
| Calibrated KSI forecast | 196.0 |
| Spearman rank corr. (forecast vs. EB benchmark) | 0.994 |
| 2-year aggregate bias (2024-2025) | +0.68% |

---

## 12. Empirical Bayes Stabilization

### Problem

Low-volume corridors: one unusual month makes observed severity composition look extreme.
A corridor with 1 fatal crash out of 3 KSI total appears to have 100% fatal composition.
This would distort CMF-based benefit calculations.

### Solution

EB shrinkage pulls each corridor's severity composition toward the network-wide mean:

    p_EB(i, s) = [n(i,s) + tau * p_network(s)] / [n(i) + tau]

    i = corridor, s = severity class, tau = precision parameter

As observed volume n(i) increases, the corridor's own proportions dominate.
For low-volume corridors, the estimate is pulled toward the network mean.

**Verified:** Severity shrinkage shares sum to 1.0 across all 43 corridors.

**Scope:** EB stabilizes crash composition only. It does not create a traffic-exposure denominator.

---

## 13. Treatment Applicability

### Evaluation Results

| Treatment ID | Name | Status | Reason |
|---|---|---|---|
| **TRT_001** | **Pedestrian Refuge Islands** | **PROVISIONAL** | CMF and cost verified; physical geometry pending |
| **TRT_002** | **Road Diet (4-to-3 Lane)** | **PROVISIONAL** | CMF and cost verified; lane count data pending |
| **TRT_004** | **RRFB at Uncontrolled Crossing** | **PROVISIONAL** | CMF and cost verified; crossing inventory pending |
| TRT_003 | Speed Feedback Signs | BLOCKED | CMF unverified for long-term corridor reduction |
| TRT_005 | High-Friction Treatment (Curve) | BLOCKED | Curve geometry and friction data unavailable |
| TRT_006 | High-Friction Treatment (Ramp) | BLOCKED | Ramp inventory unavailable |

**Physical applicability is UNKNOWN for all active treatments.** Lane counts, ADT, median widths,
and crossing inventories are not available from current open spatial datasets. Every selected
project requires CDOT/IDOT engineering review.

### Target Crash Filtering

Each CMF is applied only to the crash population it is documented to affect:

- TRT_001, TRT_004: Pedestrian crashes only
- TRT_002: All crash types

Applying a pedestrian CMF to all crashes would overstate benefits. Enforced by pipeline and tests.

---

## 14. Crash Modification Factors

All CMFs from FHWA CMF Clearinghouse, star rating >= 4 (high-quality evidence).

| Treatment | ID | CMF | Reduction | Stars | Target | Cost (Base 2024) | Life |
|---|---|---|---|---|---|---|---|
| TRT_001 Refuge Island | 175 | 0.68 | 32% | 4 | Pedestrian crashes | $15,000/location | 20 yr |
| TRT_002 Road Diet | 3006 | 0.71 | 29% | 5 | All crashes | $400,000/corridor-mile | 20 yr |
| TRT_004 RRFB | 9024 | 0.53 | 47% | 4 | Pedestrian crashes | $22,500/crossing | 10 yr |

Uncertainty scenarios: CONSERVATIVE (upper CI bound), BASE (point estimate), OPTIMISTIC (lower CI).

CMF limitation: These are national study estimates. Local Chicago effectiveness may differ.

---

## 15. Benefit-Cost Analysis

### Formulas

    Crashes Averted(i,j)   = Forecast Applicable Crashes(i,j) x (1 - CMF(j))

    Annual Benefit(i,j)    = Sum[Crashes Averted(i,j,s) x Unit Crash Cost(s)]
                             (Unit costs from USDOT 2024 BCA guidance, by KABCO class)

    PV Benefit(i,j)        = Annual Benefit(i,j) x [1 - (1+r)^(-Life(j))] / r

    BCR(i,j)               = PV Benefit(i,j) / PV Capital Cost(i,j)

### Critical Distinction

**BCR is a descriptive metric only. The MILP optimizer maximizes total PV benefit, not BCR.**
Maximizing BCR biases selection toward cheap treatments on high-crash corridors and is prohibited
by Decision D023.

### Verified Aggregate (Base Scenario, All 43 x 3 Candidates)

| Metric | Value |
|---|---|
| Total benefit scenario rows | 387 (43 x 3 treatments x 3 uncertainty levels) |
| Aggregate PV benefit | $6.55B |
| Aggregate capital cost | $26.75M |
| Aggregate candidate BCR | ~245:1 |
| Critical failures in BCA validation | 0 |

---

## 16. Portfolio Optimization

### Decision Variable

    x(i,j) in {0,1}
    i = corridor (1...43), j = treatment {TRT_001, TRT_002, TRT_004}
    x(i,j) = 1 means treatment j selected for corridor i

### Objective

    Maximize  Sum  PV_Benefit(i,j) * x(i,j)

### Constraints

| Constraint | Rule |
|---|---|
| Budget ceiling | Total cost <= Budget |
| Equity floor | Equity spend / Total selected spend >= Floor |
| One treatment per corridor | Sum_j x(i,j) <= 1 for all i |
| Non-trivial portfolio | Sum x(i,j) >= 1 |
| Road Diet concentration cap (D026) | Road Diet selections <= 70% of total |
| Functional-class exclusion (D027) | Road Diet = 0 for expressways/divided carriageways |
| Economic viability (D023) | BCR >= 1.0 required for eligibility |

### Solver and Results

**Engine:** scipy.optimize.milp (HiGHS C++ branch-and-cut)
**All 192 scenario runs:** OPTIMAL status verified
**Determinism:** 3 independent repeat solves per scenario -- 100% SHA-256 hash match

---

## 17. System Architecture

```
+----------------------------------------------------------+
|                  RAW DATA SOURCES                        |
|  Chicago Crashes API  Vehicles API  People API           |
|  Street Center Lines  CDC SVI 2022  FHWA CMF Evidence    |
+------------------------+---------------------------------+
                         |
                         v
+----------------------------------------------------------+
|           DATA VALIDATION & CLEANING                     |
|  KABCO mapping  Deduplication  Coordinate validation     |
|  Vehicle-to-crash aggregation                            |
+------------------------+---------------------------------+
                         |
                         v
+----------------------------------------------------------+
|         SPATIAL CORRIDOR CONSTRUCTION                    |
|  43-corridor register  Geometry from Street Center Lines |
|  EPSG:4326->EPSG:3435  R-Tree indexing                  |
|  100-ft assignment rule (D017)  Zero reconciliation diff |
+------------------------+---------------------------------+
                         |
                         v
+----------------------------------------------------------+
|          43 x 96 CORRIDOR-MONTH PANEL                    |
|  4,128 rows  2018-2025  112,421 assigned crashes         |
+------------------------+---------------------------------+
                         |
           +-------------+--------------+
           v                            v
+-------------------+     +-------------------------+
| TOTAL CRASH MODEL |     |     KSI CRASH MODEL     |
| 12-Month Rolling  |     | Negative Binomial GLM   |
| Mean Benchmark    |     | + Empirical Bayes (EB)  |
+--------+----------+     +-------------+-----------+
         +-------------------+          |
                             v
+----------------------------------------------------------+
|          2026 CORRIDOR CRASH RISK FORECAST               |
|  516 predictions  Total: 14,029.8  KSI: 196.0           |
|  Zero future leakage  Spearman rank corr: 0.994         |
+------------------------+---------------------------------+
                         |
                         v
+----------------------------------------------------------+
|       TREATMENT APPLICABILITY & CMF ECONOMICS            |
|  3 active treatments  387 scenario rows                  |
|  FHWA CMF (4-5 star)  USDOT 2024 crash costs            |
|  Target-crash filtering  20-year PV calculation          |
+------------------------+---------------------------------+
                         |
                         v
+----------------------------------------------------------+
|          MILP PORTFOLIO OPTIMISATION                     |
|  scipy.optimize.milp / HiGHS solver                     |
|  192 scenarios  100% OPTIMAL  Deterministic             |
+------------------------+---------------------------------+
                         |
         +---------------+---------------+
         v               v               v
  +----------+    +-----------+    +-----------+
  |STREAMLIT |    | POWER BI  |    |    n8n    |
  |Scenario  |    |Executive  |    | QA-gated  |
  |Planner   |    |Dashboard  |    | Delivery  |
  +----------+    +-----------+    +-----------+
```

**Data layers:**
- `data/raw/` -- IMMUTABLE source snapshots, never modified
- `data/interim/` -- Cleaned and spatially assigned working files
- `data/processed/` -- Validated analytical outputs (parquet + CSV)

**CRS:** All distance calculations in EPSG:3435 (Illinois State Plane East, feet).
Degree-based distance calculation is explicitly prohibited.

---

## 18. Technology and Tools

| Tool | Role | Why Selected |
|---|---|---|
| Python 3.13 | Primary analytical pipeline | Reproducible, open-source, ecosystem depth |
| pandas / NumPy | Data transformation | Standard tabular + array operations |
| GeoPandas / Shapely | Spatial processing | Native GeoDataFrame, EPSG:3435 support |
| pyproj | CRS reprojection | Accurate linear-unit distance |
| statsmodels | Poisson and NB GLM | Count-data regression diagnostics |
| scikit-learn | Evaluation metrics | Consistent MAE / RMSE / deviance |
| scipy.optimize.milp | MILP optimization (HiGHS) | Globally optimal binary integer solution |
| DuckDB / SQL | Analytical queries | In-process columnar queries |
| QGIS | Corridor geometry QA | Visual spatial inspection |
| Streamlit | Scenario planner | Python-native, Community Cloud deployment |
| Power BI | Executive reporting | PBIX with DAX measures |
| n8n | QA-gated delivery automation | Visual workflow, governance checkpoints |
| pytest | 327 automated acceptance tests | Contract-level verification per stage |
| Git / GitHub | Version control | Exact run-state traceability |
| joblib | Model serialization | Production artifact portability |

---

## 19. Streamlit Application

**URL:** [vision-zero-chicago-charan.streamlit.app](https://vision-zero-chicago-charan.streamlit.app/)

The Streamlit application provides an interactive interface for planners and stakeholders to
explore portfolio results and run custom scenarios.

### Page 1 -- Executive Recommendation

Selected corridors, treatment recommendation, capital cost, and expected PV benefit for a
chosen budget and equity scenario. Portfolio summary: total cost, PV benefit, BCR, equity share.
Governance audit log: constraints met, warnings, governance labels.

[PENDING SCREENSHOT -- capture Page 1 from live app at vision-zero-chicago-charan.streamlit.app]

### Page 2 -- Portfolio Overview

Scenario comparison across official budget/equity combinations. PV benefit by scenario, budget
utilization, equity share vs. floor, Road Diet concentration.

[PENDING SCREENSHOT -- capture Page 2]

### Page 3 -- Corridor Explorer

Corridor-level detail: 2026 forecast crash burden (total and KSI), treatment recommendation and BCR,
corridor severity history, equity classification.

[PENDING SCREENSHOT -- capture Page 3]

### Page 4 -- Governance / Methodology

Full transparency layer: governance warnings from each pipeline stage, assumption register,
methodology summary, limitations and responsible use statement.

[PENDING SCREENSHOT -- capture Page 4]

### Testing

Verified by test_streamlit_dashboard.py (AppTest functional scenarios) and
test_streamlit_deployment.py. Both pass with zero critical failures.

---

## 20. Power BI Dashboard

[PENDING SCREENSHOT -- capture from Power BI Desktop or published report]

The Power BI dashboard provides a fixed-format reporting view for City leadership and planning
meetings. It connects to `data/processed/` parquet outputs via DuckDB SQL views.

Key views: portfolio summary by scenario, corridor-level ranked investment table, equity spending
analysis, budget sensitivity chart, governance status panel.

Unlike Streamlit, Power BI does not run live MILP optimization. All visuals reflect pre-computed,
validated pipeline outputs.

---

## 21. n8n Automation

[PENDING SCREENSHOT -- export from n8n]

The n8n workflow provides QA-gated controlled delivery of portfolio outputs.

**Workflow:**
1. Pipeline completion trigger
2. QA gate: verify critical_failure_count = 0 in all validation JSONs
3. If QA passes: proceed to delivery (report generation, notification)
4. If QA fails: halt delivery, alert analyst

No analytical output is delivered to stakeholders before pipeline QA passes.

---

## 22. Testing and Quality Assurance

### Test Suite

**23 test files, 327 automated acceptance tests.** All critical failures: 0.

| Test File | Pipeline Stage |
|---|---|
| test_project_setup.py | Environment and dependencies |
| test_spatial_acquisition.py | Street Center Lines and spatial sources |
| test_spatial_contract.py | Corridor geometry construction |
| test_corridor_register.py | 43-corridor register counts, keys |
| test_corridor_geometry.py | Geometry length, completeness, CRS |
| test_crash_cleaning.py | Crash cleaning and severity mapping |
| test_crash_validation.py | Deep crash record validation |
| test_cleaning_contract.py | Cleaning contract compliance |
| test_primary_crash_assignment.py | 100-ft rule, 4-category reconciliation |
| test_crash_assignment.py | Assignment output schema and counts |
| test_corridor_month_panel.py | 4,128-row panel, severity reconciliation |
| test_corridor_month_features.py | Feature engineering, leakage prevention |
| test_crash_risk_models.py | Rolling-origin protocol, model selection |
| test_2026_corridor_risk_forecast.py | 516-row forecast, calibration checks |
| test_treatment_readiness.py | Treatment eligibility, equity classification |
| test_treatment_benefits.py | 387-row benefits, PV reconciliation |
| test_portfolio_optimization.py | 192-scenario portfolio, constraints |
| test_threshold_sensitivity.py | Buffer sensitivity (50/100/150 ft) |
| test_decision_mart.py | Python vs. SQL cross-tool reconciliation |
| test_sql_analytics_mart.py | DuckDB schema and row-count contracts |
| test_streamlit_dashboard.py | Streamlit AppTest functional scenarios |
| test_streamlit_deployment.py | Deployment environment |
| conftest.py | Shared fixtures and infrastructure |

### QA Summary

| Metric | Result |
|---|---|
| Critical validation failures (all stages) | **0** |
| MILP solver statuses (192 runs) | **100% OPTIMAL** |
| Repeat-solve SHA-256 hash match | **100%** |
| Severity reconciliation diff | **0** |
| Budget constraint violations | **0** |
| Equity floor violations | **0** |
| Duplicate primary crash assignments | **0** |
| Duplicate corridor assignments per portfolio | **0** |

---

## 23. Results and Findings

All figures sourced from validated pipeline outputs. No planning assumptions or estimates used.

### Spatial Assignment

112,421 crashes uniquely assigned to the 43 corridors under the 100-foot rule.
Four-category reconciliation difference: **0**.

### Model Selection

**Total crashes:** 12-Month Rolling Mean selected over all GLM and ML alternatives.
Validation Poisson deviance 1.648, MAE 5.22, calibration ratio 0.984.

**KSI crashes:** Negative Binomial GLM + EB shrinkage selected. Post-EB validation calibration
ratio **1.000**, correcting the uncalibrated 25.84% overprediction bias.

### 2026 Forecast

14,029.8 total crashes and 196.0 KSI crashes forecast across 43 corridors.
Rank correlation with EB benchmark: Spearman 0.994.

### Portfolio: $15M / BASE / 20% Equity (Binding Budget Scenario)

| Metric | Verified Value |
|---|---|
| Corridors funded | 39 of 43 |
| Capital allocated | $14,988,510 (~$14.99M) |
| Budget slack | $11,490 (effectively binding) |
| High-SVI equity spending share | 47.35% (floor: 20%) |
| Annual KSI crashes avoided | **48.04 per year** |
| Annual total crashes avoided | **2,170.20 per year** |
| 20-year PV safety benefit | **$4.00B** |
| Benefit-cost ratio | **267.12:1** |

### Portfolio: $25M and $40M Scenarios

Under conservative unit-cost assumptions, treating all 43 corridors costs at most $17.56M (BASE).
Both $25M and $40M planning budgets are non-binding. All 43 corridors are selected. Same portfolio
selection regardless of whether the budget ceiling is $25M or $40M.

**This is a documented governance finding.** The $15M budget scenario is the only official scenario
where the budget constraint is binding and forces project trade-offs.

### Key Governance Findings

| Finding | Implication |
|---|---|
| All official budgets non-binding except $15M | Budget sensitivity requires binding stress scenarios ($2M-$6M) |
| All equity floors non-binding | Unconstrained optimal selection concentrates in equity-priority corridors |
| Road Diet concentration 68.8% (cap: 70%) | Diversification constraint approaching binding threshold |
| Physical applicability UNKNOWN | Engineering field review required before any project advances |

---

## 24. Social and Industry Relevance

### For City Government and Transportation Planning

This project demonstrates how open public data can support transparent, reproducible capital
prioritization. Analytical assumptions are explicit, testable, and auditable.

Key value:
- Defensible shortlist for community and council review
- Equity requirement built into optimization rather than applied as afterthought
- Scenario comparison makes trade-offs visible
- Reproducible pipeline allows annual refresh as new crash data becomes available

### For Transportation Safety Analysts

This project goes beyond descriptive analysis:

- Spatial analytics: coordinate-accurate crash assignment
- Statistical forecasting: count models, rolling-origin validation
- Optimization: constrained portfolio selection
- Evidence synthesis: CMF literature + economic valuation

The methodology is transferable to any city with open crash data and published corridor definitions.

### For Data Science Practitioners

Key analytical lessons:

- Why a rolling mean beat GLM and ML on this dataset (and why that is a valid result)
- How EB shrinkage addresses small-sample instability in count composition
- How vehicle-to-crash aggregation prevents a common count-inflation error
- How MILP formulation differs from greedy ranking
- How governance warnings differ from pipeline failures -- and why both matter

---

## 25. Limitations and Responsible Use

### This System Is Not

- An automatic capital project approval system
- A real-time crash prediction tool
- Official City of Chicago policy
- A replacement for engineering field surveys or community engagement
- A causal study of treatment effectiveness in Chicago
- A procurement or construction authorization system

### Documented Limitations

| Category | Limitation |
|---|---|
| Candidate set | 43 corridors from 2018 HCC Plan only |
| Traffic exposure | No reliable AADT; crash burden not exposure-normalized (A007) |
| Crash coordinates | GPS offset uncertainty unquantified; 0.81% lack coordinates |
| Treatment costs | Analyst-defined planning scenarios; must be updated with Chicago bid prices (A005) |
| CMF validity | National studies; no local Chicago calibration (A004) |
| Physical applicability | Lane counts, median widths, crossing inventories unavailable |
| Economic benefits | Societal crash costs per USDOT -- not City cash savings |
| Equity classification | SVI overlap threshold; community preferences outside model |
| Forecast stationarity | Assumes roadway geometry unchanged |
| Causal inference | Does not establish causal treatment effects in Chicago |

All 9 formal assumptions with status and sensitivity flags: `docs/assumption_register.csv`.

---

## 26. Learning and Reflection

### Technical Skills Developed

| Skill | Application |
|---|---|
| SQL | DuckDB analytical queries, serving views for Power BI |
| Python / pandas | Full analytical pipeline from acquisition to optimization |
| Spatial analytics | GeoPandas corridor geometry, EPSG reprojection, R-Tree indexing |
| Statistical forecasting | Rolling-origin GLM evaluation, count model selection |
| Empirical Bayes | Shrinkage estimation for sparse count data |
| Optimization | MILP formulation, constraint specification, solver interpretation |
| Power BI | DAX measures, directquery connection to parquet outputs |
| Streamlit | Live Python app deployment with MILP integration |
| Automated testing | pytest contract-level verification of each analytical stage |
| n8n | Visual workflow automation with QA-gated delivery |

### Analytical Learning

The most significant learning was understanding when a problem is a ranking problem and when it is
an allocation problem.

I initially approached this as a corridor ranking problem: score corridors, sort them, fund the
top N within budget. During development I recognized this framework cannot answer the actual
question. A ranking does not account for:

- One cheap treatment on a medium-crash corridor can deliver more benefit per dollar than an
  expensive treatment on the highest-crash corridor
- Equity spending must be a share of selected spending, not a fixed set
- Treatment suitability differs by corridor -- Road Diet is inappropriate on Lake Shore Drive
  regardless of crash count

This led to the redesign around treatment applicability, benefit-cost analysis, and portfolio
optimization.

### Governance Learning

Treating warnings as evidence rather than problems to eliminate. The governance warning that all
official planning budgets are non-binding is the most important finding in the project. A system
designed only to produce clean passes would have suppressed this information. Preserving it is
what makes the output trustworthy.

### Personal Reflection

This project changed how I think about the boundary between analysis and decision-making.
The system produces numbers with high precision. Those numbers are built on planning-cost
assumptions not verified by Chicago engineers, CMFs from studies in other states, and a spatial
algorithm that will place some crashes on the wrong corridor.

Communicating limitations explicitly -- as first-class governance findings, not footnotes --
is part of what makes the analysis credible rather than merely impressive-looking. A stakeholder
who finds a limitation later is far more damaging to trust than a limitation acknowledged upfront.

---

## 27. Future Scope

None of the following are implemented in the current system.

| Extension | Description |
|---|---|
| HCC refresh | Update to post-2018 High-Crash Corridor designations |
| Traffic exposure | Continuous AADT for exposure-normalized crash rates |
| Additional treatments | Signal timing, crossing consolidation, protected intersections |
| Construction timing | Phased capital programming with scheduling constraints |
| Maintenance costs | Annual maintenance and residual value in lifecycle BCA |
| Non-safety co-benefits | Travel time, emissions, active transportation mode shift |
| Network connectivity | Segment-level interdependencies and barrier-effect reduction |
| Community preferences | Participatory input on priorities and treatment preferences |
| Probabilistic uncertainty | Monte Carlo treatment-effect uncertainty propagation |
| Post-implementation evaluation | Before-after comparison framework |

Future scope does not imply planned features. These are potential analytical directions.

---

## 28. Conclusion

Vision Zero Chicago demonstrates how data analytics can transform road-safety investment from a
subjective exercise into a transparent, reproducible, and governable decision-support process.

The system combines six analytical layers -- spatial crash assignment, time-series forecasting,
Empirical Bayes stabilization, evidence-based CMF benefit estimation, lifecycle present-value
analysis, and constrained portfolio optimization -- into a connected pipeline that answers a
precise question:

> Which corridor-treatment projects should be shortlisted for engineering review to maximize
> expected safety benefit under a defined budget and equity requirement?

The answer under the $15M conservative planning budget: **39 of 43 corridors**, with an expected
**$4.00B in present-value safety benefit** (267:1 BCR), **48 KSI crashes avoided per year**, and
**47% of capital directed to high-vulnerability communities**.

These figures are planning estimates. They are built on provisional unit costs, national CMF
evidence, and physical applicability assumptions not verified by engineering field survey.

The system's value is that it makes the analytical method, the assumptions, the limitations, and
the governance warnings **visible and auditable** -- so that engineers, planners, and community
representatives can engage with the analysis rather than accept it as a black box.

Engineering feasibility, community engagement, procurement, and final budget authority remain
human responsibilities. The system is designed to make those conversations better informed,
not to replace them.

---

## 29. GitHub and Project Resources

**Live Streamlit Dashboard:** [vision-zero-chicago-charan.streamlit.app](https://vision-zero-chicago-charan.streamlit.app/)

**GitHub Repository:** [CharanKumar17-a/vision-zero-chicago](https://github.com/CharanKumar17-a/vision-zero-chicago)

### Key Output Files

| File | Description |
|---|---|
| `data/processed/portfolio_scenario_summary.parquet` | 192-scenario portfolio summary |
| `data/processed/portfolio_project_selections.parquet` | Individual project selections |
| `data/processed/corridor_treatment_benefits.parquet` | 387-row treatment benefit scenarios |
| `outputs/forecasts/corridor_risk_forecast_2026.parquet` | 2026 monthly corridor forecast |
| `outputs/forecasts/corridor_risk_forecast_2026_annual.csv` | 2026 annual corridor forecast |
| `outputs/tables/model_comparison.csv` | Forecasting model comparison results |
| `docs/data_quality/` | 30+ pipeline validation JSON files |
| `docs/submission/model_card.md` | Forecasting model card |
| `docs/submission/solver_audit.md` | MILP solver audit |
| `docs/audits/upstream_analytical_audit.md` | Phase-2 upstream analytical audit |

### Local Setup

```powershell
Set-Location "D:\data-analytics\vision-zero-chicago"
.venv\Scripts\Activate.ps1
.venv\Scripts\python.exe -m pytest tests/ -v
.venv\Scripts\python.exe -m streamlit run dashboard/streamlit/app.py
```

---

## 30. References

| Reference | Role |
|---|---|
| City of Chicago. (2018). Vision Zero Chicago: High-Crash Corridor Framework Plan. | Candidate corridor definitions |
| Chicago Data Portal. Traffic Crashes - Crashes (85ca-t3if). | Primary crash records |
| Chicago Data Portal. Traffic Crashes - Vehicles (68nd-jvt3). | Crash unit flags |
| Chicago Data Portal. Traffic Crashes - People (u6pd-qa9d). | Injury classification |
| Chicago Data Portal. Street Center Lines (6imu-meau). | Corridor geometry source |
| CDC/ATSDR. (2022). Social Vulnerability Index - Illinois Census Tracts. | Equity area designation |
| FHWA CMF Clearinghouse. ID 175. Pedestrian Refuge Islands. FHWA-HRT-08-041 / NCHRP 617. | TRT_001 CMF (4-star, 32% reduction) |
| FHWA CMF Clearinghouse. ID 3006. Road Diet Safety Evaluation. FHWA-HRT-10-053. | TRT_002 CMF (5-star, 29% reduction) |
| FHWA CMF Clearinghouse. ID 9024. RRFB at Unsignalized Crossings. NCHRP Report 841. | TRT_004 CMF (4-star, 47% reduction) |
| USDOT. (2024). Benefit-Cost Analysis Guidance for USDOT Projects. | KABCO unit crash costs |
| Huangfu, Q. & Hall, J.A.J. (2018). Parallelizing the dual revised simplex method. Math. Prog. Comp. | HiGHS MILP solver |
| EPSG:3435. Illinois State Plane East. | Projected CRS for distance calculations |
| Vision Zero Network. (2024). Vision Zero in the United States: City Action Plans. | Programme context |

---

## 31. Appendices

### Appendix A -- Assumption Register

Source: `docs/assumption_register.csv`

| ID | Category | Assumption | Status | Sensitivity |
|---|---|---|---|---|
| A001 | Scope | Candidate set contains 43 corridors | Validated | No |
| A002 | Temporal | 96 complete monthly periods Jan 2018 - Dec 2025 | Validated | Yes |
| A003 | Spatial | 100-ft buffer is operational primary assignment threshold | Validated | Yes |
| A004 | Treatment | Published CMFs support planning estimates | Pending validation | Yes |
| A005 | Economic | Published treatment costs support planning scenarios | Pending validation | Yes |
| A006 | Equity | Transparent equity constraint can be evaluated | Pending validation | Yes |
| A007 | Exposure | Historical crash counts represent recorded burden, not exposure-normalized risk | Active limitation | No |
| A008 | Data maturity | Incomplete 2026 period excluded from historical modelling | Validated rule | Yes |
| A009 | Spatial | Rows without coordinates excluded from corridor assignment | Validated rule | Yes |

### Appendix B -- Data Quality Pipeline Summary

All critical failures: **0** across all pipeline stages.

| Stage | Validation File | Status |
|---|---|---|
| Source acquisition | acquisition_contract_validation.json | PASS |
| Crash cleaning | crash_cleaning_validation.json | PASS |
| Deep crash validation | crash_core_deep_validation.json | PASS |
| Corridor register | corridor_register_validation.json | PASS |
| Corridor geometry | corridor_geometry_validation.json | PASS |
| Crash spatial assignment | crash_corridor_assignment_validation.json | PASS |
| Corridor-month panel | corridor_month_panel_validation.json | PASS |
| Corridor-month features | corridor_month_features_validation.json | PASS |
| Crash risk models | crash_risk_model_validation.json | PASS_WITH_WARNINGS |
| 2026 forecast | corridor_risk_forecast_2026_validation.json | PASS |
| Treatment readiness | treatment_readiness_validation.json | PASS_WITH_WARNINGS |
| Treatment benefits | treatment_benefits_validation.json | PASS_WITH_WARNINGS |
| Portfolio optimisation | portfolio_optimization_validation.json | PASS_WITH_WARNINGS |
| Decision mart | decision_output_mart_validation.json | PASS |
| SQL analytics mart | sql_analytics_mart_validation.json | PASS |
| Streamlit dashboard | streamlit_dashboard_validation.json | PASS |

### Appendix C -- CMF Evidence Summary

| Treatment | Source | CMF | 95% CI | Stars | Sample |
|---|---|---|---|---|---|
| Refuge Islands (TRT_001) | FHWA-HRT-08-041 / NCHRP 617 | 0.68 | 0.61-0.75 | 4 | 124 sites |
| Road Diet (TRT_002) | FHWA-HRT-10-053 | 0.71 | 0.66-0.76 | 5 | 84 corridors |
| RRFB (TRT_004) | NCHRP Report 841 | 0.53 | 0.47-0.59 | 4 | 312 crossings |

### Appendix D -- Portfolio Governance Warnings

Source: `portfolio_optimization_validation.json`

| Warning Code | Summary | Governance Ref |
|---|---|---|
| WARNING_OFFICIAL_BUDGETS_NONBINDING | All official budgets exceed maximum corridor treatment cost | D004, D005 |
| WARNING_OFFICIAL_PORTFOLIOS_IDENTICAL | All 27 official runs select the same 43 projects | D004, D005 |
| WARNING_ROAD_DIET_CONCENTRATION | 68.8% of selected projects are Road Diet (cap: 70%) | A004, D005, D026 |
| WARNING_EQUITY_FLOORS_NONBINDING | Unconstrained selection achieves 45.18% equity naturally | D004, D005 |
| WARNING_ANALYST_DEFINED_STRESS_BUDGETS | $2M/$4M/$6M are diagnostic scenarios, not City budgets | D004, D005 |
| WARNING_EXTREME_BCR | Some individual BCRs exceed 1,000 due to planning-cost assumptions | A005, D005 |
| WARNING_PHYSICAL_APPLICABILITY_UNKNOWN | All selected projects require engineering review | A004, D005 |

---

*Document prepared for SURE Trust Data Analytics G1 Capstone, September 2026.*
*All analytical claims sourced to validated pipeline outputs in `docs/data_quality/`.*
*Governance record: `docs/decision_log.csv`. Reproducibility: see README.md.*
