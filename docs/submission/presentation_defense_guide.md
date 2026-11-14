# Vision Zero Chicago — Master Presentation & Defense Guide
## Complete Spoken Script, Business Rationale, Terminology, Chart Walkthroughs & Technical Defense
**Author:** B. Charan Kumar | **Mentor:** Nithyasri | **Program:** Data Analytics G1, SURE Trust | **Date:** September 2026

---

# Part 1: High-Level Presentation Architecture & Flow

This document is your master playbook for presentations, capstone defense, and technical interviews. It covers word-for-word spoken scripts, business problem mappings, terminology translations, visual/diagram walkthroughs, page-by-page web application demonstrations, and tough examiner Q&A.

### The 4-Stage Presentation Flow
1. **The Hook & Problem Framing (Slides 1–4 / ~3 mins):** The municipal dilemma: 877k crashes vs limited capital. Why historical crash ranking is fundamentally flawed (severity-blind, cost-blind, equity-blind).
2. **Data & Spatial Engineering (Slides 5–8 / ~4 mins):** Integrating 8 open datasets, preventing join inflation (Decision D002), 100-foot buffer in Illinois State Plane East (EPSG:3435), and zero-diff 4-category reconciliation.
3. **Forecasting, Stabilization & Optimization (Slides 9–14 / ~6 mins):** Why rolling-origin evaluation beat complex ML for total crashes; Negative Binomial + Empirical Bayes shrinkage for KSI crashes; FHWA CMF economics; Mixed-Integer Linear Programming (MILP) allocating the $15M budget.
4. **Product, Governance & Impact (Slides 15–20 / ~5 mins):** Live 4-page Streamlit application walkthrough, Power BI executive view, automated n8n QA pipeline, 327 passing unit tests, and defense of governance warnings.

---

# Part 2: Section-by-Section Presentation Script & Deep Dive

---

## 1. Title & Executive Summary (Final Report §1)

### Visual / Slide
- **Visual:** Project Title, Author (B. Charan Kumar), Mentor (Nithyasri), SURE Trust credentials, and live web app link.
- **Key Metric Callouts:** 877,919 Crash Records · 43 Corridors · 192 Optimized Portfolios · $4.00B PV Safety Benefit · 327 Tests Passed (0 Failures).

### Spoken Script (Word-for-Word)
> "Good morning, esteemed mentors, evaluators, and colleagues. My name is B. Charan Kumar, and today I am presenting **Vision Zero Chicago: Automated Safety Capital Investment Prioritization System**, developed as my capstone project under the mentorship of Nithyasri at SURE Trust.
>
> In public administration and urban engineering, leadership faces a continuous dilemma: between 2018 and 2025, the City of Chicago recorded over 877,000 traffic collisions. However, municipal capital budgets are strictly limited. The City cannot afford to rebuild every roadway at once.
>
> Traditional approaches simply rank streets by past crash counts. But as data practitioners, we know that historical ranking fails: it treats a minor bumper scrape identically to a fatal pedestrian strike; it ignores how much interventions cost; it ignores whether a street can physically accommodate a treatment; and it fails to ensure equitable investments in historically underserved neighborhoods.
>
> My project solves this as a **constrained capital allocation problem**. Using an end-to-end data analytics pipeline and Mixed-Integer Linear Programming (MILP), the system evaluates 129 candidate corridor-treatment projects across Chicago's 43 official High-Crash Corridors. Under a baseline $15 Million budget, our system identifies an optimal portfolio of 39 corridor projects that delivers **$4.00 Billion in 20-year present-value societal safety benefits**, prevents an estimated **48 fatal and severe injuries per year**, and directs **47.35% of all funds to high-vulnerability communities**—with zero critical quality failures across 327 automated tests.
>
> Most importantly, this is an **analytical decision-support tool**, not an automated decision-maker. It preserves professional engineering discretion while making investment trade-offs transparent, auditable, and reproducible."

### Business Problem Addressed
- **Capital Scarcity vs Network Demand:** Cities have finite budgets ($15M, $25M, $40M) and must justify every dollar spent to community stakeholders and city council.
- **Flawed Legacy Prioritization:** Manual or simple sort-by-crash ranking misallocates millions of dollars to low-return or inequitable projects.

### Key Terminology Explained
- **Vision Zero:** An international road safety movement originating in Sweden, based on the ethical premise that no loss of life or severe injury on public streets is acceptable, shifting the primary responsibility from individual driver behavior to roadway system design.
- **Decision-Support System (DSS):** An interactive computational platform that compiles complex raw data, models, and constraints to help human decision-makers evaluate options. It aids decisions; it does not replace human engineers.
- **Societal Safety Benefit:** The quantified economic value of avoided deaths, prevented trauma surgeries, and preserved quality of life, monetized using federal USDOT economic valuations.

---

## 2. Business Decision & Problem Statement (Final Report §2–§4)

### Visual / Slide
- **Visual:** Comparison chart: "Naive Crash Ranking" (sorted list) vs "Constrained Optimization" (multi-criteria combinatorial portfolio).
- **Flow Graphic:** Candidate Network (43 Corridors) × Countermeasures (3 Treatments) → 129 Decision Variables → MILP Optimization → Single Optimal Shortlist.

### Spoken Script
> "To understand why this system was built, we must examine the exact decision City of Chicago transportation planners face every fiscal cycle:
>
> *'Given a limited capital budget and an equity mandate, which specific corridor-treatment projects should be shortlisted for engineering field review to maximize community life-safety?'*
>
> If a city simply funds the top 10 corridors with the highest crash counts, three severe analytical failures occur:
> 1. **Severity Blindness:** A corridor with 500 minor property-damage crashes ranks higher than a corridor with 50 fatal pedestrian collisions.
> 2. **Economic Inefficiency:** An expensive $5M intervention on a high-crash corridor might yield a low benefit-cost ratio, whereas three targeted $1M interventions on moderate corridors could save five times as many lives.
> 3. **Equity Neglect:** High-traffic commercial corridors in affluent areas monopolize funds, starving historically disadvantaged neighborhoods on Chicago's South and West sides.
>
> Therefore, we defined our active decision unit as a **corridor-treatment project**—one specific countermeasure applied to one specific corridor. With 43 corridors and 3 active treatments, there are up to 129 possible project candidates. Selecting the optimal combination is not a simple sorting task; it is an NP-hard combinatorial optimization problem that requires mathematical modeling."

### Business Rationale & Relevance
- **For Municipal Government:** Defensible shortlists for council hearings; transparent criteria that eliminate political favoritism.
- **For Transportation Planners:** Eliminates weeks of manual spreadsheet scenario modeling; guarantees multi-criteria compliance automatically.

---

## 3. Data Sources & Quality Engineering (Final Report §6–§7)

### Visual / Slide
- **Visual:** Relational diagram connecting Crashes, Vehicles, People, Street Centerlines, CDC SVI, and FHWA CMFs.
- **Table:** 4-Category Spatial Assignment Reconciliation Table (showing 877,919 total with 0 discrepancy).

### Spoken Script
> "A model is only as credible as its underlying data. We integrated 8 authoritative public sources without relying on proprietary or private data:
> - Over **1.08 million** raw crash records from the City of Chicago Open Data Portal (2018–2025).
> - Detailed **Vehicles** (2.2M rows) and **People** (2.3M rows) relational tables.
> - **Chicago Street Center Lines** (56,338 segments) for physical road geometry.
> - The **2018 Chicago High-Crash Corridor Framework Plan** for candidate boundaries.
> - **CDC/ATSDR 2022 Social Vulnerability Index (SVI)** for census tract equity metrics.
> - **FHWA CMF Clearinghouse** and **USDOT 2024 BCA Guidance** for treatment effectiveness and crash costs.
>
> Here we resolved a critical data engineering challenge documented in our Decision Log as **Decision D002**:
> In open crash data, a single collision often involves multiple vehicles and pedestrians. If an analyst joins the Vehicle or People tables directly to the Crash table, it creates a one-to-many join that artificially duplicates crash records, inflating crash counts by over 100%!
>
> To eliminate this, our pipeline enforces strict pre-aggregation: vehicle-level and person-level attributes are aggregated into crash-level binary flags—such as `is_pedestrian` or `is_hit_and_run`—*before* joining back to the primary crash entity.
>
> Furthermore, we established a mathematically closed **4-Category Reconciliation**: out of 877,919 cleaned records:
> - Exactly **112,421 crashes** (13.12%) were assigned to our 43 High-Crash Corridors.
> - **1,803 crashes** (0.21%) were flagged as ambiguous multi-corridor intersection ties.
> - **756,545 crashes** (86.88%) fell outside the corridor buffer.
> - **7,150 crashes** (0.81%) lacked valid geographic coordinates and were preserved rather than silently deleted.
>
> The sum of these four categories equals 877,919 with an exact **zero-record reconciliation discrepancy**."

### Key Terminology Explained
- **One-to-Many Join Inflation:** A relational database hazard where joining child rows (vehicles) to a parent row (crash) duplicates parent rows, causing false counts unless child records are pre-aggregated.
- **KABCO Scale:** The federal standardized injury classification: K (Fatal), A (Suspected Serious Injury), B (Suspected Minor Injury), C (Possible Injury), O (Property Damage Only).
- **Data Lineage:** The complete, auditable lifecycle of data that tracks its origin, transformations, and final publication.

---

## 4. Spatial Corridor Construction & GIS Methodology (Final Report §8)

### Visual / Slide
- **Diagram:** Corridor Centerline, 100-foot buffer envelope, incident snapping, intersection tie buffer, and EPSG:3435 projection callout.
- **Chart:** Spearman rank correlation curve across 50 ft, 100 ft, and 150 ft buffer sensitivities.

### Spoken Script
> "Spatial analytics requires extreme rigor. Crash coordinates are recorded in standard GPS latitude and longitude (WGS84, EPSG:4326).
>
> A common beginner mistake is computing Euclidean distances directly on latitude and longitude degrees. Because lines of longitude converge toward the poles, one degree of longitude in Chicago is roughly 82 kilometers, while one degree of latitude is 111 kilometers. Measuring distance in degrees distorts spatial buffers into stretched ovals and skews crash counts.
>
> Our pipeline re-projects all geometries into **EPSG:3435 (Illinois State Plane East, measured in survey feet)** using GeoPandas and pyproj.
>
> Using high-performance R-Tree spatial indexing (`STRtree`), we evaluated crash-to-corridor distances. Under **Decision D017**, we established an operational **100.0-foot buffer** with a **10.0-foot tie tolerance**. If a crash falls within 100 feet of two crossing corridors within 10 feet of each other, it is marked as an unresolved tie rather than assigned arbitrarily.
>
> To defend this 100-ft choice, we conducted an offline **Spatial Sensitivity Analysis** across 50-ft, 100-ft, and 150-ft buffers:
> - The Spearman rank correlation of corridor crash counts between 50 ft and 100 ft is **0.9784**.
> - Between 100 ft and 150 ft, it is **0.9878**.
> - 38 out of 39 selected projects in our baseline portfolio remained 100% identical between 50 ft and 100 ft.
>
> This mathematically proves that our spatial assignment is rock-solid: GPS coordinate noise does not distort the investment decisions recommended by the system."

### Key Terminology Explained
- **EPSG:3435:** The official conformal coordinate system for Illinois East, preserving local distances and angles with linear units in survey feet.
- **STRtree (Sort-Tile-Recursive R-Tree):** A 2D spatial index that groups geometric objects into hierarchical bounding boxes, reducing spatial point-in-polygon queries from $O(N)$ brute-force to $O(\log N)$ logarithmic speed.
- **Spearman Rank Correlation ($r_s$):** A non-parametric statistical metric measuring monotonic relationship between rankings. A score above 0.97 demonstrates that the relative priority order of corridors does not change with buffer size.

---

## 5. Longitudinal Panel & Predictive Risk Modeling (Final Report §11)

### Visual / Slide
- **Matrix Graphic:** 43 Corridors × 96 Months = 4,128 row panel structure.
- **Evaluation Chart:** Model comparison bar chart showing Poisson Deviance and MAE across Seasonal Naive, 12-Month Rolling Mean, Poisson GLM, and Negative Binomial GLM.

### Spoken Script
> "Once crashes were spatially linked, we structured our historical baseline into a balanced longitudinal panel of **43 corridors across 96 months (January 2018 through December 2025)**, totaling exactly **4,128 monthly observations**.
>
> Across 8 years, only 7 out of 4,128 corridor-months recorded zero crashes—proving that these corridors suffer from chronic, persistent risk rather than isolated flukes.
>
> To forecast 2026 crash risk, we rejected random cross-validation. In time-series forecasting, random splits allow future data to leak into past predictions. Instead, we instituted a **strict chronological rolling-origin evaluation protocol**:
> - 2018: Warm-up & lag initialization
> - 2019–2023: Training split (2,580 rows)
> - 2024: Held-out validation split for model selection (516 rows)
> - 2025: True hindsight test backtest (516 rows)
> - 2026: Out-of-sample planning forecast horizon (516 predictions)
>
> Here is a finding that demonstrates true engineering honesty:
> For **Total Crashes**, the **12-Month Historical Rolling Mean** outperformed all complex regression and machine learning models on the validation split, achieving the lowest Poisson deviance of **1.648**, an MAE of **5.22**, and a near-perfect calibration ratio of **0.984**. We selected this benchmark transparently rather than artificially forcing an overfitted machine learning model.
>
> However, for **KSI (Fatal and Serious Injury) crashes**, the data exhibited extreme zero-inflation—61.6% of corridor-months had zero severe injuries—and severe overdispersion. Here, standard Poisson regression failed, and the **Negative Binomial GLM** won with a validation Poisson deviance of **0.988**."

### Key Terminology Explained
- **Look-Ahead Bias (Data Leakage):** An analytical flaw where information from the future (e.g., 2025 crash trends) is inadvertently included in training features, producing unrealistically optimistic backtest metrics.
- **Overdispersion:** A statistical condition where the variance of count data exceeds its mean. Standard Poisson regression assumes variance equals mean ($\mathrm{Var}(Y) = \mathrm{E}(Y)$); when overdispersion is present, Poisson models underestimate standard errors and overfit.
- **Negative Binomial GLM:** A generalized linear model for count data that includes a gamma-distributed dispersion parameter, specifically designed for overdispersed Poisson processes.

---

## 6. Empirical Bayes (EB) Shrinkage Stabilization (Final Report §12)

### Visual / Slide
- **Formula Graphic:** Empirical Bayes shrinkage equation with callouts for corridor observations ($n$), prior weight ($\tau$), and network mean ($p_{\text{network}}$).
- **Graphic:** Visual showing low-volume corridor estimates being pulled toward the citywide average.

### Spoken Script
> "Why couldn't we use the raw Negative Binomial KSI output directly for calculating economic benefits?
>
> On the validation split, the raw Negative Binomial model overpredicted aggregate KSI crashes by 25.84%. Furthermore, severe crashes on individual corridors are statistically sparse. If Corridor A has only 2 fatal crashes in 8 years, a single tragic collision could double its observed rate, causing severe regression-to-the-mean distortion.
>
> To solve this, we implemented **Empirical Bayes (EB) Shrinkage Calibration**, following Highway Safety Manual best practices:
>
> $$\text{p}_{EB}(i, s) = \frac{n(i, s) + \tau \cdot p_{\text{network}}(s)}{n(i) + \tau}$$
>
> Empirical Bayes acts as a Bayesian shrinkage operator:
> - For corridors with large crash volumes, the observed data dominates, and the estimate stays close to the corridor's empirical rate.
> - For low-volume corridors with high variance, the estimate is smoothly shrunk toward the reliable network-wide average.
>
> Applying EB shrinkage brought our validation KSI calibration ratio from an uncalibrated 1.258 directly to **1.000**. In our 2025 out-of-sample backtest, the net two-year aggregate prediction bias across the entire network was an extraordinary **+0.68%**."

### Business Rationale & Relevance
- **Prevents Capital Misallocation:** Prevents a city from spending $1M on a quiet street that just happened to have an anomalous, uncharacteristic severe crash during a single year.

---

## 7. Treatment Countermeasures & CMF Evidence Matrix (Final Report §13–§14)

### Visual / Slide
- **Visual:** Countermeasure visual cards showing Refuge Islands, Road Diets, and RRFBs with FHWA star ratings, CMF values, unit costs, and service lives.

### Spoken Script
> "Next is treatment engineering. We surveyed six potential countermeasures. Three were blocked due to missing physical inventories: Speed Feedback Signs, High-Friction Surface Treatments on curves, and HFST on ramps.
>
> We retained three provisional countermeasures supported by FHWA 4-star and 5-star evidence:
> 1. **TRT_001: Pedestrian Refuge Islands & Raised Medians:** Documented under FHWA Clearinghouse ID 175 (4-star). It delivers a **32% reduction in pedestrian crashes** ($\text{CMF} = 0.68$), with a base planning cost of $15,000 per location and a 20-year service life.
> 2. **TRT_002: Road Diet (4-to-3 Lane Conversion):** Documented under FHWA ID 3006 (5-star). It converts four undivided travel lanes into two travel lanes, a continuous center turn lane, and dedicated bike/pedestrian space. It delivers a **29% reduction in all corridor crashes** ($\text{CMF} = 0.71$), with a base cost of $400,000 per corridor-mile and a 20-year service life.
> 3. **TRT_004: Rectangular Rapid Flashing Beacons (RRFB):** Documented under FHWA ID 9024 (4-star). Installed at uncontrolled marked crossings, it delivers a **47% reduction in pedestrian crashes** ($\text{CMF} = 0.53$), costing $22,500 per crossing with a 10-year service life.
>
> Here we enforced strict **Target-Crash Filtering**:
> TRT_001 and TRT_004 reduce *pedestrian* crashes only. If an analyst applies their CMF to *all* corridor crashes—including rear-ends and sideswipes—benefits would be falsely inflated by 800%. Our code strictly isolates pedestrian crashes before multiplying by $(1 - \text{CMF})$."

### Key Terminology Explained
- **Crash Modification Factor (CMF):** A multiplicative index estimating the expected crash frequency after implementing a countermeasure relative to baseline. A CMF of 0.71 represents a $1 - 0.71 = 29\%$ expected reduction.
- **Road Diet:** A roadway reconfiguration converting a four-lane undivided road into two travel lanes, a center turn lane, and shoulder/bike facilities, eliminating left-turn conflicts and reducing severe vehicle speed differentials.
- **RRFB (Rectangular Rapid Flashing Beacon):** Pedestrian-actuated high-intensity amber strobe lights mounted on crosswalk signs that increase driver yielding rates from ~20% to over 85%.

---

## 8. Lifecycle Benefit-Cost Analysis (BCA) (Final Report §15)

### Visual / Slide
- **Formulas:** Crashes Averted, Annual Societal Benefit, Present Value discounting formula, and BCR equation.
- **Table:** USDOT 2024 Comprehensive Crash Cost breakdown by KABCO class.

### Spoken Script
> "To translate averted crashes into economic terms, we implemented official **USDOT 2024 Benefit-Cost Analysis Guidance**.
>
> Safety benefits are calculated using KABCO comprehensive societal crash costs:
> - Fatal Crash (K): **$13.2 Million**
> - Suspected Serious Injury (A): **$760,000**
> - Minor Injury (B): **$165,000**
> - Possible Injury (C): **$86,000**
> - Property Damage Only (O): **$6,200**
>
> For each corridor $i$ and treatment $j$, we compute:
> 1. **Annual Crashes Averted:** 
>    $$\Delta \text{Crashes}_{i,j} = \text{Forecast Target Crashes}_i \times (1 - \text{CMF}_j)$$
> 2. **Annual Societal Dollar Benefit:**
>    $$\text{Annual Benefit}_{i,j} = \sum_s \Delta \text{Crashes}_{i,j,s} \times \text{Unit Cost}_s$$
> 3. **20-Year Net Present Value (NPV):**
>    $$\text{PV Benefit}_{i,j} = \text{Annual Benefit}_{i,j} \times \left[ \frac{1 - (1 + r)^{-\text{Life}_j}}{r} \right]$$
>    using the federal $r = 7.0\%$ discount rate.
>
> Across all 387 corridor-treatment-uncertainty combinations, candidate projects represent $26.75M in total capital needs and over $6.55 Billion in aggregate societal benefits."

### Critical Defense: Defending the 267:1 BCR
> "Mentors and evaluators will inevitably ask: *'Why is your portfolio BCR 267 to 1? Isn't that extraordinarily high?'*
>
> The defense is three-fold:
> 1. **Comprehensive Societal Cost vs Cash Savings:** The $13.2M federal valuation for a fatal crash reflects the statistical value of human life (VSL), lost lifetime economic productivity, medical trauma care, and family grief. It is **societal preservation**, not cash municipal revenue.
> 2. **Planning Striping Costs:** Countermeasures like road diets ($400k/mile) are low-cost re-striping and signage treatments applied to dense urban arterials carrying 15,000 vehicles daily. Preventing even 2 severe pedestrian injuries over 20 years easily outweighs a $400,000 paint-and-post countermeasure.
> 3. **BCR is Descriptive, Not the Objective:** The optimizer does **not** maximize BCR. Maximizing BCR would prioritize tiny, cheap striping on minor streets. We maximize total Net Present Societal Benefit."

---

## 9. Mixed-Integer Linear Programming (MILP) Optimization (Final Report §16)

### Visual / Slide
- **Mathematical Formulation Box:**
  - Objective: $\max \sum_{i} \sum_{j} \text{PV\_Benefit}_{i,j} \cdot x_{i,j}$
  - Subject to: Budget Ceiling, Equity Spending Floor, Mutual Exclusivity, Road Diet Cap, Functional Class Exclusions.
- **Table:** 192 Solved Scenarios (27 Official, 9 Stress, 156 Grid) all reporting OPTIMAL status.

### Spoken Script
> "Now we arrive at the decision core: the mathematical optimization engine.
>
> We formulate project prioritization as a **Mixed-Integer Linear Program (MILP)** solved using `scipy.optimize.milp` backed by the high-performance HiGHS C++ branch-and-cut solver.
>
> Let $x_{i,j} \in \{0, 1\}$ be a binary decision variable where $x_{i,j} = 1$ if treatment $j$ is funded on corridor $i$, and $0$ otherwise.
>
> **Objective Function:**
> Maximize total 20-year present-value safety benefit across all selected projects:
> $$\max \sum_{i=1}^{43} \sum_{j} \text{PV\_Benefit}_{i,j} \cdot x_{i,j}$$
>
> Subject to 5 governed constraints:
> 1. **Mutual Exclusivity:** $\sum_j x_{i,j} \le 1 \quad \forall i$. At most one capital project is awarded per corridor. You cannot build a Road Diet and a Refuge Island on the exact same road segment simultaneously.
> 2. **Planning Budget Ceiling:** $\sum_{i} \sum_j \text{Cost}_{i,j} \cdot x_{i,j} \le \text{Budget}$. Total capital cost cannot exceed available funds.
> 3. **Equity Spending Floor:**
>    $$\sum_{i \in \text{HighSVI}} \sum_j \text{Cost}_{i,j} \cdot x_{i,j} \ge \text{Floor} \times \sum_{i} \sum_j \text{Cost}_{i,j} \cdot x_{i,j}$$
>    Notice that the denominator is **total selected project spending**, not the budget ceiling. This guarantees that real dollars spent are distributed equitably.
> 4. **Road Diet Diversification Cap (Decision D026):**
>    $$\sum_{i} x_{i, \text{RoadDiet}} \le 0.70 \times \sum_i \sum_j x_{i,j}$$
>    Prevents countermeasure monoculture by capping road diets at 70% of selected projects.
> 5. **Functional Class Feasibility (Decision D027):**
>    $x_{\text{LakeShoreDrive}, \text{RoadDiet}} = 0$. You cannot physically apply a 4-to-3 lane conversion on an 8-lane grade-separated arterial like DuSable Lake Shore Drive!
>
> Across 192 scenario solves, every single solve reached verified **OPTIMAL** status, with **100% deterministic repeat-solve SHA-256 hash matching**."

---

## 10. Key Analytical Findings & Budget Bindingness (Final Report §23)

### Visual / Slide
- **Chart:** Budget vs Benefit Frontier curve ($2M to $40M), highlighting the $15M binding point and the $17.56M plateau.
- **Summary Cards:** $15M Baseline: 39 corridors selected, $14.99M allocated, $11,490 slack, 47.35% equity, $4.00B PV benefit.

### Spoken Script
> "The optimization produced a profound governance insight:
>
> - Under the **$15 Million Baseline Budget**, the budget constraint is **strictly binding**. The optimizer allocates **$14,988,510** (leaving just $11,490 in unallocated slack), funding **39 out of 43 corridors**. It forces real, mathematically defensible trade-offs, funding the 39 projects that maximize life-saving return.
> - However, under the **$25 Million and $40 Million Budgets**, the budget becomes **non-binding**. Why? Because treating all 43 candidate corridors under our baseline planning costs requires only **$17.56 Million**. Once all 43 corridors receive their optimal treatment, the system cannot spend additional money because of the mutual exclusivity constraint!
> - Similarly, the **Equity Spending Floors (20%, 30%, 40%)** are naturally non-binding: the unconstrained baseline selection naturally directs **45.18% to 47.35%** of spending to high-SVI communities because Chicago's severe crash burden is heavily concentrated in historically underserved South and West side wards.
>
> In an uncritical project, someone might claim they generated 27 completely different portfolios for each scenario. We documented this as a formal governance finding: official budgets above $17.56M select the identical complete 43-project portfolio. To evaluate true constrained behavior, we created 9 diagnostic stress budgets at $2M, $4M, and $6M."

---

## 11. Software Engineering, QA & Automation (Final Report §17–§18, §21–§22)

### Visual / Slide
- **Terminal Snippet:** `pytest tests/` output: `327 passed, 0 failures in 532.30s (0:08:52)`.
- **Diagram:** n8n automated delivery workflow with QA gate node (`critical_failure_count == 0`).

### Spoken Script
> "To ensure production-grade reproducibility, our workspace adheres to a strict analytical contract:
> - **327 automated acceptance tests** in pytest, organized across 23 test suites.
> - Confirmed in our test run: **327 passed, 0 failed** in 8 minutes and 52 seconds.
> - **16 formal automated quality validation JSON artifacts** in `docs/data_quality/`, tracking critical failure counts (exactly 0 across the entire pipeline).
> - Clean architectural separation:
>   - Core analytical pipeline in Python 3.13 (`src/`).
>   - Analytical serving marts in DuckDB SQL (`sql/`).
>   - Web user interface in Streamlit (`dashboard/streamlit/`).
>   - Executive dashboard in Power BI (`dashboard/powerbi/`).
>   - QA-gated delivery automated through n8n workflows (`automation/n8n/`)."

---

## 12. Live Streamlit Web Application Walkthrough (Final Report §19)

### Visual / Slide
- **Live Browser / Mockup:** Walkthrough of the 4 deployed pages on [vision-zero-chicago-17a.streamlit.app](https://vision-zero-chicago-17a.streamlit.app/).

### Spoken Script (Page by Page)

#### Page 1: Executive Recommendation
> "When stakeholders open our application, Page 1 provides the primary answer-first decision interface:
> - In the sidebar, planners select their **Planning Budget ($15M, $25M, $40M)**, **Equity Spending Floor (20%, 30%, 40%)**, and **CMF Uncertainty Tier (Conservative, Base, Optimistic)**.
> - At the top, 4 dynamic KPI cards display: **Selected Projects (39)**, **Allocated Capital ($14.99M)**, **20-Year PV Benefit ($4.00B)**, and **Achieved Equity Share (47.35%)**.
> - Below, an interactive Leaflet map renders the 43 High-Crash Corridors color-coded by selected treatment (green for Road Diets, blue for Refuge Islands, orange for RRFBs).
> - An expandable **Governance Audit Log** alerts planners that physical applicability remains UNKNOWN and requires engineering field surveys."

#### Page 2: Portfolio Overview
> "Page 2 is designed for executive leadership comparing scenarios:
> - It features multi-scenario comparison charts showing how societal safety benefits scale from $2M stress budgets up to $40M.
> - A Pareto frontier scatter plot contrasts Capital Expenditure against Net Present Benefit.
> - An equity compliance radar confirms whether portfolios satisfy the City's racial and economic equity mandates."

#### Page 3: Corridor Explorer
> "Page 3 serves CDOT project engineers drilling down into a single corridor:
> - A user can select any corridor—for example, `HCC027 Western Ave (31st St to 55th St)`.
> - The page displays its 8-year historical crash trend, monthly seasonality, severity breakdown, and its 2026 forecast baseline.
> - It presents a side-by-side comparison of all candidate treatments, explaining why TRT_002 Road Diet was chosen over TRT_001 Refuge Islands based on BCR and crash reduction potential."

#### Page 4: Governance & Methodology
> "Page 4 is the transparent scientific record:
> - It exposes the complete **Decision Log** (from D001 through D027).
> - It publishes the live **Assumption Register**, detailing all 9 active assumptions and their sensitivity statuses.
> - It links directly to GitHub repository source code, pipeline validation JSONs, and FHWA reference literature."

---

## 13. Limitations, Ethics & Responsible AI Boundaries (Final Report §25)

### Visual / Slide
- **Visual:** The 7 Responsible-Use Boundaries checklist.

### Spoken Script
> "A hallmark of professional data science is knowing what your model *cannot* do. We explicitly document 7 responsible-use boundaries:
> 1. **No Real-Time Prediction:** This models annual planning risk, not tomorrow's collision.
> 2. **No Automated Approvals:** Every recommendation is provisional until civil engineers conduct sight-line, curb-radius, and utility surveys.
> 3. **Physical Applicability UNKNOWN:** Current open datasets lack continuous lane counts and median widths. We refuse to fake these attributes; we label them UNKNOWN.
> 4. **Planning Costs vs Contractor Bids:** Sourced from national averages; local prevailing wages and Chicago material costs will require localized estimation.
> 5. **No Individual Profiling:** The model predicts roadway risk, not individual driver behavior, avoiding discriminatory predictive policing.
> 6. **Societal Value vs City Revenue:** $4 Billion is the economic value of preserved human life, not cash savings.
> 7. **No Official Policy Claim:** This is an independent academic capstone project developed with SURE Trust, not official City of Chicago legislation."

---

## 14. Conclusion & Future Roadmap (Final Report §27–§28)

### Visual / Slide
- **Visual:** Summary takeaway cards + Future Research Roadmap (AADT sensors, construction phasing, participatory budgeting).

### Spoken Script
> "To conclude, **Vision Zero Chicago** demonstrates how data analytics bridges the gap between raw open data and transparent capital governance.
>
> By transforming a naive ranking problem into a constrained Mixed-Integer Linear Program, we prove that a targeted $15 Million investment can avert 48 fatal and severe injuries annually, generate $4 Billion in community safety value, and guarantee equitable investment in Chicago's most vulnerable neighborhoods.
>
> In future phases, this framework can integrate continuous Average Daily Traffic (AADT) sensor counts, multi-year construction phasing, and community participatory budgeting.
>
> Thank you to my mentor Nithyasri, SURE Trust, and this panel. I am now open to your questions."

---

# Part 3: Complete Terminology & Concepts Master Table

| Term | Plain-English Definition | Why It Matters for Decision-Makers | Why It Matters for You in an Interview |
| :--- | :--- | :--- | :--- |
| **Vision Zero** | International policy initiative to eliminate all traffic fatalities and severe injuries through safe systems design. | Establishes the political, moral, and federal justification for prioritizing life-safety over traffic speed. | Proves your project aligns with real-world municipal policy and USDOT Safe Streets for All (SS4A) grants. |
| **High-Crash Corridor (HCC)** | An arterial roadway segment showing a disproportionately high concentration of fatal and serious-injury crashes. | Focuses limited capital on the top 10% of street mileage where 50%+ of severe injuries happen. | Shows you understand proper spatial grain definition (corridor vs. intersection vs. citywide). |
| **KABCO Scale** | Standardized police severity scale: Fatal (K), Incapacitating (A), Non-incapacitating (B), Possible Injury (C), Property Damage Only (O). | Weights life-safety outcomes over minor fender-benders in benefit calculations. | Demonstrates familiarity with federal highway safety data standards. |
| **KSI** | "Killed or Seriously Injured" ($K + A$). | The primary benchmark metric used by transportation safety agencies worldwide. | Demonstrates domain knowledge in transportation safety performance measurement. |
| **EPSG:3435** | Illinois State Plane East coordinate system, projected in linear survey feet. | Ensures accurate distance measurements in feet without latitude/longitude degree distortion. | Shows advanced GIS engineering competence beyond basic lat/lon mapping. |
| **R-Tree / STRtree** | Multi-dimensional spatial tree index that bounds geometries in minimum bounding rectangles. | Accelerates spatial querying from hours to milliseconds across 877k rows. | Demonstrates algorithmic optimization and scalability awareness. |
| **Look-Ahead Bias (Data Leakage)** | When future information inadvertently contaminates model training data. | Guarantees that historical models don't unrealistically over-perform. | Shows rigorous machine learning validation standards. |
| **Rolling-Origin Cross-Validation** | Chronological evaluation moving forward year-by-year without random shuffling. | Reflects how models operate in reality (predicting future from past). | Differentiates rigorous time-series data science from naive Kaggle-style splits. |
| **Poisson Deviance** | Goodness-of-fit loss metric comparing observed counts to Poisson model predictions. | Evaluates count models appropriately without assuming normal Gaussian errors. | Proves you choose loss functions tailored to discrete count data distributions. |
| **Overdispersion** | When the variance of a count variable is significantly greater than its mean. | Standard Poisson models fail when data is overdispersed; requires Negative Binomial. | Shows deep statistical understanding of count data regression. |
| **Empirical Bayes (EB) Shrinkage** | Method pooling corridor observations with network-wide priors to stabilize sparse rates. | Eliminates extreme small-sample noise and regression-to-the-mean bias. | Signals mastery of Highway Safety Manual (HSM) methodology. |
| **Crash Modification Factor (CMF)** | Multiplicative factor indicating expected crash change after treatment ($< 1.0$ is a reduction). | Quantifies the scientific effectiveness of engineering countermeasures. | Shows integration of peer-reviewed empirical transportation literature. |
| **Target Crashes** | The specific collision types physically addressable by a treatment (e.g. pedestrian crossing crashes). | Prevents benefit inflation by applying pedestrian CMFs only to pedestrian collisions. | Proves analytical integrity and prevention of benefit double-counting. |
| **Road Diet** | Converting a 4-lane undivided road into 2 travel lanes, a center turn lane, and bike lanes. | High-impact treatment reducing speeding, left-turn conflict points, and pedestrian exposure. | Demonstrates familiarity with proven FHWA safety countermeasures. |
| **RRFB** | Rectangular Rapid Flashing Beacon: user-actuated amber LEDs at uncontrolled crossings. | Increases driver yielding rates from ~20% to over 85% at crosswalks. | Shows multi-modal safety intervention expertise. |
| **Value of Statistical Life (VSL)** | Federal economic estimate ($13.2M in 2024) of societal willingness to pay to prevent one death. | Establishes the dollar value of life-safety in public infrastructure benefit-cost analysis. | Answers why economic benefits reach billions without claiming municipal cash flow. |
| **Discount Rate ($r = 7\%$)** | The interest rate used to discount future cash flows/benefits to present value. | Accounts for the time value of money and opportunity cost of public capital. | Adheres strictly to federal OMB Circular A-94 economic standards. |
| **MILP** | Mixed-Integer Linear Programming: mathematical optimization where some variables are integers/binary. | Solves complex capital allocation problems to exact mathematical optimality. | Sets you apart from standard analysts who only know heuristic sorting. |
| **Branch-and-Cut** | Exact algorithm used by HiGHS to solve integer linear programming problems. | Guarantees finding the global optimum without evaluating all $2^{129}$ combinations. | Demonstrates deep algorithmic knowledge of computational solvers. |
| **Mutual Exclusivity** | Constraint ensuring at most one treatment is selected per corridor ($\sum_j x_{i,j} \le 1$). | Prevents building a Road Diet and Refuge Island on the exact same pavement. | Proves logical consistency in optimization constraints. |
| **SVI (Social Vulnerability Index)** | CDC metric combining 16 census variables to measure community vulnerability to hazards. | Directs safety capital to historically neglected, disadvantaged populations. | Demonstrates practical application of social equity in technical engineering. |
| **Binding Constraint** | A constraint that limits the objective value (slack equals zero at optimality). | Reveals what is genuinely restricting performance (e.g. $15M budget vs. $25M non-binding). | Shows executive-level financial and analytical intuition. |

---

# Part 4: Detailed Diagram & Chart Walkthrough Guide

### Diagram 1: End-to-End System Pipeline (Mermaid Architecture)
- **What it shows:** The continuous data flow from Raw Socrata APIs -> Cleaning & Validation -> Spatial Projection (EPSG:3435) -> 43x96 Panel -> Risk Forecasting (NB+EB) -> Treatment Economics -> MILP Solver -> Streamlit / Power BI / n8n.
- **How to explain it:** *"Follow the arrows from top to bottom. Notice that our pipeline enforces unidirectional data flow. There are no circular dependencies. Before data enters modeling, it passes through spatial contracts; before it enters the solver, it passes through CMF filtering; and before reaching the UI, it passes through automated QA gates."*

### Diagram 2: Spatial Buffer & Snapping Diagram
- **What it shows:** A road centerline with a 100-foot buffer polygon around it. Crash points inside the polygon are snapped; points within 10 feet of two intersecting corridors are marked as yellow "Unresolved Ties"; points outside are gray.
- **How to explain it:** *"Notice the green corridor centerline. The shaded region represents our 100-foot buffer in Illinois State Plane East coordinates. Point A is 45 feet away and uniquely assigned. Point B is at an intersection, 60 feet from both Corridor 1 and Corridor 2; rather than guessing and risking double-counting, our algorithm flags it as an unresolved tie. This maintains 100% auditable spatial precision."*

### Chart 3: Model Calibration & Evaluation Matrix
- **What it shows:** Validation split performance contrasting Seasonal Naive, Rolling Mean, Poisson GLM, and Negative Binomial GLM across Poisson Deviance, MAE, and Calibration Ratio.
- **How to explain it:** *"On this chart, closer to the bottom left indicates lower error and deviance. For total crashes, the blue dot representing 12-Month Rolling Mean achieves the lowest deviance (1.648) and closest calibration to 1.0 (0.984). For KSI, the purple dot representing Negative Binomial GLM achieves the lowest deviance (0.988), which is then brought to exactly 1.000 calibration via Empirical Bayes shrinkage."*

### Chart 4: Capital Allocation & Societal Benefit Frontier
- **What it shows:** A curve plotting Budget ($2M to $40M) on the X-axis and Present Value Safety Benefit on the Y-axis, showing steep linear gains from $2M to $15M, followed by a flat plateau at $17.56M.
- **How to explain it:** *"This chart illustrates the economic law of diminishing marginal returns. From $2M to $15M, every dollar invested yields massive societal returns as high-crash corridors are treated. However, between $15M and $17.56M, the curve plateaus: once all 43 corridors have received their optimal treatment, additional budget cannot produce additional safety benefits under our candidate scope. This proves why $25M and $40M budgets are non-binding."*

---

# Part 5: Master Defense: Tough Examiner & Interviewer Q&A

### Q1: "Why did you choose a simple 12-Month Rolling Mean over XGBoost, Random Forests, or Deep Learning for Total Crashes?"
> **Your Defense:**
> "In production decision-support systems, model complexity must be justified by empirical performance. On our chronological 2024 validation split, we tested gradient boosted trees and GLMs against empirical benchmarks. The 12-Month Rolling Mean achieved the lowest Poisson deviance (1.648) and lowest MAE (5.22), with a calibration ratio of 0.984.
>
> Complex non-linear models overfit to pandemic-era anomalies (2020–2021) and suffered from higher validation deviance. Furthermore, in municipal government, a transparent, defensible model that stakeholders understand is vastly superior to a black-box model that performs worse on out-of-sample data. We reported this transparently rather than artificially forcing complex ML."

### Q2: "A Benefit-Cost Ratio of 267:1 seems unrealistic. How do you defend that to City Council?"
> **Your Defense:**
> "That is a very fair and important question. In our report, we explicitly document this under Warning `WARNING_EXTREME_BCR`.
>
> There are three reasons for this figure:
> 1. **Societal Value vs. Financial Return:** Under federal USDOT guidance, a fatal collision is valued at $13.2 Million in comprehensive societal impact. Preventing just 48 fatal and severe injuries per year across 39 major urban arterials aggregates to hundreds of millions in societal preservation annually. It does not represent cash revenue.
> 2. **Planning-Level Restriping Costs:** Our baseline costs assume standard FHWA striping and signage costs ($400k/mile for road diets). If Chicago conducts full geometric reconstruction with curb replacement and stormwater drainage, costs could rise to $2M/mile, which would reduce the BCR to ~50:1.
> 3. **The Optimizer's Objective:** Most importantly, the optimizer does **not** maximize BCR. If it did, it would select trivial paint treatments on minor streets. It maximizes total Net Present Value of human lives protected."

### Q3: "Why are the $25M and $40M official budgets non-binding? Did your solver fail?"
> **Your Defense:**
> "The solver functioned with 100% mathematical optimality. The non-binding status is a finding of municipal capital analysis, not a software bug.
>
> Treating all 43 designated High-Crash Corridors under our candidate countermeasure set costs at most $17.56 Million in the BASE scenario. Because our model enforces mutual exclusivity—allowing at most one primary capital treatment per corridor to prevent over-building—the system exhausts all feasible projects at $17.56 Million.
>
> Therefore, allocating $25 Million or $40 Million leaves unallocated slack. We documented this as `WARNING_OFFICIAL_BUDGETS_NONBINDING`. It proves to city leadership that if they have $40 Million to spend, they should expand the candidate corridor network beyond the 43 historical corridors or consider higher-cost physical streetscape overhauls."

### Q4: "What is the difference between a Poisson GLM and Negative Binomial GLM, and why did it matter for KSI crashes?"
> **Your Defense:**
> "A standard Poisson distribution assumes equidispersion, meaning the variance equals the mean ($\mathrm{Var}(Y) = \mathrm{E}(Y)$).
>
> In our monthly corridor panel, KSI crashes had a mean of 0.55 crashes/month but a variance of 1.18, with 61.6% zero-months. This overdispersion violates Poisson assumptions and causes standard errors to be severely underestimated. The Negative Binomial GLM introduces an additional dispersion parameter $\alpha$ that models the variance as $\mathrm{Var}(Y) = \mu + \alpha \mu^2$, properly accounting for excess zeros and rare, clustering fatal events."

### Q5: "Why did you mark Physical Applicability as UNKNOWN? Why didn't you just assign the treatments?"
> **Your Defense:**
> "Marking physical applicability as UNKNOWN is an ethical and engineering safeguard.
>
> A Road Diet physically requires an undivided 4-lane cross-section with an Average Daily Traffic (ADT) typically under 20,000 vehicles. While our spatial linework gives us corridor centerline length, open city portals do not currently provide continuous lane counts, turn-lane geometries, or midblock curb widths.
>
> Faking or assuming these geometric values would be dangerous: it could lead to recommending a road diet on a corridor that is already 2 lanes or an 8-lane divided highway. By explicitly setting applicability to UNKNOWN and flagging `WARNING_PHYSICAL_APPLICABILITY_UNKNOWN`, our system provides a prioritization shortlist while mandating that CDOT/IDOT field engineers verify site geometry before capital programming."

---
*Guide compiled for B. Charan Kumar's SURE Trust Capstone Defense & Technical Interviews, September 2026.*
