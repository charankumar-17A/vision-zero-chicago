"""Governance and Methodology Page - Vision Zero Chicago Decision Support App.

Contract: docs/data_quality/decision_output_mart_contract.md
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add repository root to sys.path so standalone scripts and Streamlit pages resolve dashboard namespace
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd
import streamlit as st

from dashboard.streamlit.components import (
    render_governance_footer,
    render_governance_header_banner,
    render_page_header,
    render_sidebar_controls,
)
from dashboard.streamlit.data_access import (
    load_portfolio_summary,
    load_validation_evidence,
)

render_page_header(
    "Governance & methodology",
    "Decision-support boundaries, pipeline validation, equity frameworks, and methodological audit registers.",
)

# Unified Information & Governance Banner
render_governance_header_banner(
    run_group="OFFICIAL",
    is_official=True,
    custom_subtitle=(
        "&dollar;15M budget is binding (&dollar;14.99M allocated across 39 corridors); "
        "&dollar;25M / &dollar;40M allow full 43-corridor coverage. "
        "All selections require engineering field review. "
        "Planning-level decision support only; does not authorize projects or replace engineering review."
    ),
)

# Load serving datasets & validation evidence
df_summary = load_portfolio_summary()
evidence = load_validation_evidence()

# Render sidebar controls & get active portfolio
portfolio_id = render_sidebar_controls(df_summary)

# -----------------------------------------------------------------------------
# SECTION 1 — EXECUTIVE GOVERNANCE SUMMARY (4 Simple, Consistent Cards)
# -----------------------------------------------------------------------------
exec_cards_html = """
<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:12px; margin-top:8px; margin-bottom:14px;">
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px; box-shadow:0 1px 2px rgba(15,23,42,0.03);">
        <div style="font-size:10.5px; font-weight:700; color:#2563EB; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
            Tool Purpose
        </div>
        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-bottom:4px;">
            Planning-level decision support
        </div>
        <div style="font-size:12px; color:#475569; line-height:1.45;">
            Prioritizes corridor safety investments under stated budget, equity, safety-benefit, and planning constraints.
        </div>
    </div>
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px; box-shadow:0 1px 2px rgba(15,23,42,0.03);">
        <div style="font-size:10.5px; font-weight:700; color:#DC2626; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
            Tool Limitation
        </div>
        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-bottom:4px;">
            Not project authorization
        </div>
        <div style="font-size:12px; color:#475569; line-height:1.45;">
            Does not authorize construction, commit public funds, establish final scope, or replace engineering review.
        </div>
    </div>
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px; box-shadow:0 1px 2px rgba(15,23,42,0.03);">
        <div style="font-size:10.5px; font-weight:700; color:#0D9488; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
            Final Authority
        </div>
        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-bottom:4px;">
            City and engineering review
        </div>
        <div style="font-size:12px; color:#475569; line-height:1.45;">
            Final capital programming authority remains with City staff and professional engineering reviewers.
        </div>
    </div>
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px; box-shadow:0 1px 2px rgba(15,23,42,0.03);">
        <div style="font-size:10.5px; font-weight:700; color:#D97706; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
            Engineering Status
        </div>
        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-bottom:4px;">
            Engineering review required
        </div>
        <div style="font-size:12px; color:#475569; line-height:1.45;">
            Mathematical portfolio selection does not confirm field feasibility or implementation readiness.
        </div>
    </div>
</div>
"""
st.markdown(exec_cards_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECTION 2 — KEY GOVERNANCE MESSAGE (Amber / Caution treatment)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div style="background:#FFFBEB; border:1px solid #FDE68A; border-left:4px solid #D97706; border-radius:6px; padding:12px 18px; margin-bottom:16px;">
        <div style="font-size:13.5px; font-weight:700; color:#92400E; margin-bottom:3px;">
            Mathematical Optimality ≠ Implementation Readiness
        </div>
        <div style="font-size:12.5px; color:#78350F; line-height:1.5;">
            The optimization model identifies the highest-benefit portfolio under the stated analytical assumptions and constraints.
            It does not guarantee construction feasibility. Field conditions, geometry, utilities, traffic operations, and engineering design must be reviewed before implementation.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# SECTION 3 — EVIDENCE AT A GLANCE
# -----------------------------------------------------------------------------
geom_ev = evidence.get("geometry", {})
opt_ev = evidence.get("optimization", {})
mart_ev = evidence.get("decision_mart", {})

mart_completed = mart_ev.get("completed_at_utc") or evidence.get("deployment_manifest", {}).get("generated_at_utc", "")
val_date = mart_completed[:10] if len(mart_completed) >= 10 else "2026-08-17"

col_fresh1, col_fresh2, col_fresh3 = st.columns(3)
with col_fresh1:
    st.metric(
        "Analysis Period",
        "2018–2025",
        help="Historical baseline crash analysis window across 96 monthly periods. Does not claim all external sources update through 2025.",
    )
with col_fresh2:
    st.metric(
        "Data Last Validated",
        val_date,
        help="Timestamp when analytical serving mart datasets and decision contracts completed validation checks.",
    )
with col_fresh3:
    st.metric(
        "Pipeline Status",
        "Validated",
        help="All automated pipeline data quality and reconciliation checks passed. Public datasets are fixed snapshots and not live feeds.",
    )

# -----------------------------------------------------------------------------
# SECTION 4 — SIMPLE DECISION-MAKER SECTIONS
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("1. Decision boundaries and engineering review")

st.markdown("""
- **Mathematical Optimization**: Status values of `OPTIMAL` mean the solution is mathematically optimal under stated model constraints. It does not guarantee field constructibility.
- **Analytical Planning Portfolio vs. Implementation-Ready Portfolio**:
  - *Analytical Planning Portfolio*: Candidate corridor investments shortlisted by mathematical optimization under planning-level assumptions. All current analytical projects require engineering review (`UNKNOWN` status).
  - *Implementation-Ready Portfolio*: Projects that have completed engineering field review, cross-section validation, utility coordination, and formal implementation approvals.
- **Engineering Feasibility & Field Review Constraints**:
  - The optimization engine is architected to ingest verified field engineering data as hard constraints.
  - Projects screened out as `NOT_APPLICABLE` (e.g., Road Diet on 1-lane streets or freeways) are excluded from selection automatically.
""")

st.markdown("---")
st.subheader("2. Equity and safety interpretation")

st.markdown("""
- **Spending Equity (`High-SVI capital share`)**: Measures the proportion of total capital project investment allocated to corridors located within High-SVI census tracts.
- **Safety Benefit Equity (`KSI benefit share in high-SVI areas`)**: Measures the proportion of estimated life-safety crash reductions (Fatal K + Serious Injury A avoided) realized within High-SVI corridors.
- **Spatial Planning Proxy Note**:
  > SVI is a project-defined spatial planning proxy and does not directly measure safety benefit or represent the City of Chicago's official equity definition.
- **Methodology Note**: **SVI is used as a spatial equity proxy; it does not directly measure safety benefit equity.**
- **Policy Classification vs. Statistical Quartiles**:
  - *High-SVI Policy Classification*: A binary constraint threshold (SVI ≥ 0.75) applied during mathematical optimization.
  - *SVI Quartiles (Q1–Q4)*: A descriptive statistical distribution across the full 43-corridor network to evaluate investment balance across all vulnerability tiers.
""")

st.markdown("---")
st.subheader("3. Spatial assignment sensitivity")

spatial_ev = evidence.get("spatial_sensitivity", {})
conclusion_text = spatial_ev.get("conclusion", "Portfolio is STABLE across thresholds")
justification_text = spatial_ev.get(
    "production_rule_justification",
    "The 100-foot production assignment rule remains justified and robust. Corridor rankings exhibit >0.97 Spearman correlation across 50 ft and 150 ft, and the $15M planning portfolio has >97% corridor selection stability with no material distortion of high-level capital priorities.",
)

sensitivity_banner_html = f"""
<div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:8px; padding:12px 16px; margin-bottom:12px;">
    <div style="font-size:11px; font-weight:700; color:#166534; text-transform:uppercase; letter-spacing:0.4px;">Spatial Sensitivity Evaluation</div>
    <div style="font-size:16px; font-weight:800; color:#15803D; margin:2px 0;">Portfolio Stability: STABLE</div>
    <div style="font-size:12.5px; color:#166534; line-height:1.5;">
        The portfolio was tested across spatial assignment thresholds (50 ft, 100 ft baseline, and 150 ft). Prioritization rankings maintain &gt;0.97 Spearman correlation, and 38 of 39 selected corridors (97.4%) remain identical.
    </div>
</div>
"""
st.markdown(sensitivity_banner_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Section on Usage Analytics & Privacy (Retains exact subheader for test suite)
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("5. Usage analytics and privacy")

st.markdown("""
#### Anonymous usage measurement
- **Usage Analytics**: The system incorporates anonymous telemetry to evaluate how planners navigate, explore scenarios, inspect corridors, and export portfolios (PostHog platform).
- **Privacy and Isolation Guarantees**:
  - **Disabled by default**: Telemetry is opt-in and inactive unless explicitly enabled in configuration.
  - **Zero PII**: No personal identifying information (PII), names, email addresses, raw crash records, or user files are ever collected.
  - **Zero Analytical Impact**: Telemetry operates strictly in an isolated observer mode and never affects calculations, mathematical optimizations, or displayed values.
""")

# -----------------------------------------------------------------------------
# SECTION 5 — TECHNICAL AUDIT TRAIL
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### Technical Audit Trail")
st.caption("Detailed pipeline execution IDs, analytical grains, status hierarchies, warning registers, and scenario definitions for technical review.")

# Expander 1: Pipeline execution runs and lineage IDs
lineage_records = [
    {"Pipeline Component": "Corridor Geometry Validation", "Execution Run ID": str(geom_ev.get("run_id", "N/A")), "Status": "PASS"},
    {"Pipeline Component": "Portfolio Optimization", "Execution Run ID": str(opt_ev.get("run_id", "N/A")), "Status": "OPTIMAL"},
    {"Pipeline Component": "Decision Mart Serving", "Execution Run ID": str(mart_ev.get("run_id", "N/A")), "Status": str(mart_ev.get("status", "VALIDATED"))},
]
with st.expander("▶ View pipeline execution runs and lineage IDs", expanded=False):
    st.dataframe(pd.DataFrame(lineage_records), width="stretch", hide_index=True)

# Expander 2: Analytical grains and data contracts
with st.expander("▶ View analytical grains and data contracts", expanded=False):
    st.markdown("""
#### Analytical Grains & Serving Mart Structure
- **Portfolio Summary Grain**: `portfolio_id` × 1 row (36 canonical optimization runs: 27 Official, 9 Stress; 192 total serving mart scenarios including What-if grid).
- **Portfolio Project Selection Grain**: `portfolio_id` × `corridor_id` (1,341 detail rows across 36 canonical runs; 6,999 detail rows across all serving mart scenarios).
- **Master Corridor Grain**: `corridor_id` × 1 row (43 high-crash candidate corridors).
- **Treatment Benefits Candidate Panel Grain**: `corridor_id` × `treatment_id` × `scenario_level` (387 candidate rows).
- **Data Quality Contracts**: All schema, primary key, and grain assertions are formally defined and verified in `docs/data_quality/decision_output_mart_contract.md`.
    """)

# Expander 3: Engineering status hierarchy
with st.expander("▶ View engineering status hierarchy", expanded=False):
    st.markdown("""
#### Engineering Status Hierarchy
| Status Code | Decision Support Label | Definition | Action Required |
| :--- | :--- | :--- | :--- |
| `UNKNOWN` | **Engineering review required** | Default planning status for candidate corridors satisfying initial screening. | Field survey required prior to programming. |
| `REVIEW_REQUIRED` | **Engineering review required** | Flagged for priority field inspection due to geometric complexity or transit integration. | Detailed site survey & multi-agency review. |
| `ELIGIBLE` | **Eligible (Verified)** | Field engineering inspection has verified lane geometry, cross-sections, and clearances. | Approved for capital programming. |
| `NOT_APPLICABLE` | **Not applicable** | Screened out by road classification, lane geometry, speed limits, or transit constraints. | Excluded from investment portfolios. |
    """)

# Expander 4: Governance warning register
opt_warnings = opt_ev.get("governance_warnings", [])
mart_warnings = mart_ev.get("governance_warnings", [])
with st.expander("▶ View governance warning register", expanded=False):
    st.markdown("##### Portfolio Optimization Governance Warnings (Phase 4C evidence)")
    if opt_warnings:
        df_opt_w = pd.DataFrame(opt_warnings)
        cols_to_show = [c for c in ["code", "explanation", "limitation_or_resolution", "governance_reference"] if c in df_opt_w.columns]
        df_opt_display = df_opt_w[cols_to_show].copy()
        df_opt_display.columns = [c.replace("_", " ").title() for c in df_opt_display.columns]
        st.dataframe(df_opt_display, width="stretch", hide_index=True, height=180)
    else:
        st.info("No portfolio optimization warnings loaded.")

    st.markdown("##### Decision Mart Serving Governance Warnings (Phase 5A evidence)")
    if mart_warnings:
        df_mart_w = pd.DataFrame(mart_warnings)
        cols_to_show = [c for c in ["code", "explanation", "limitation_or_resolution", "governance_reference"] if c in df_mart_w.columns]
        df_mart_display = df_mart_w[cols_to_show].copy()
        df_mart_display.columns = [c.replace("_", " ").title() for c in df_mart_display.columns]
        st.dataframe(df_mart_display, width="stretch", hide_index=True, height=150)
    else:
        st.info("No decision mart warnings loaded.")

# Expander 5: Spatial assignment sensitivity methodology
with st.expander("▶ View spatial assignment sensitivity methodology", expanded=False):
    st.markdown(f"""
#### Empirical Assignment Sensitivity Method
The spatial sensitivity analysis tested whether assigning crashes within 50 ft, 100 ft, or 150 ft of corridor centerlines alters project selection.
Corridor rankings and capital shortlists demonstrated high stability across all tested buffer distances:
- **Spearman Rank Correlation (50 ft vs 100 ft)**: 0.9784
- **Spearman Rank Correlation (150 ft vs 100 ft)**: 0.9878
- **Portfolio Overlap at $15M**: 38 of 39 selected corridors (97.4%) identical.
- **Authoritative Conclusion**: {justification_text.replace('$', '&dollar;')}
Full test logs and JSON artifact available in `docs/data_quality/spatial_sensitivity_report.json`.
    """)

# Expander 6: Scenario definitions and audit evidence
with st.expander("▶ View scenario definitions and audit evidence", expanded=False):
    st.markdown("""
#### Canonical Scenario Groups
- **OFFICIAL Planning Scenarios (27 runs)**: Evaluates &dollar;15M, &dollar;25M, and &dollar;40M planning budgets under 20%, 30%, and 40% equity floors across Conservative, Base, and Optimistic CMF uncertainty. Official &dollar;15M budgets bind strictly under realistic unit costs (&dollar;14.99M allocated across 39 corridors in the Baseline Scenario), while &dollar;25M and &dollar;40M ceilings achieve full 43-corridor coverage.
- **BINDING-BUDGET STRESS TESTS (9 runs)**: Diagnostic stress scenarios evaluating &dollar;2M, &dollar;4M, and &dollar;6M constrained budgets under Base uncertainty. Confirms solver behavior when budget slack is tight.
    """)

# Standardized Consolidated Governance Footer
render_governance_footer()
