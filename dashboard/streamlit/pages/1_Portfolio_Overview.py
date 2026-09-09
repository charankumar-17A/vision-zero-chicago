"""Portfolio Overview Page - Vision Zero Chicago Decision Support App.

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
import plotly.graph_objects as go
import streamlit as st

from dashboard.streamlit.components import (
    format_bcr_compact,
    format_count_compact,
    format_currency,
    format_currency_compact,
    format_engineering_status,
    format_equity_flag,
    format_ksi_compact,
    format_percent,
    render_governance_footer,
    render_governance_header_banner,
    render_page_header,
    render_sidebar_controls,
)
from dashboard.streamlit.data_access import (
    evaluate_portfolio_scenario,
    load_corridor_master,
    load_portfolio_summary,
    load_treatment_benefits,
)

render_page_header(
    "Portfolio overview",
    "Planning-level decision support for provisional high-crash corridor treatment portfolios.",
)

# Load serving datasets
df_summary = load_portfolio_summary()
df_master = load_corridor_master()
df_benefits = load_treatment_benefits()

# Render sidebar controls & get active scenario parameters
scenario_params = render_sidebar_controls(df_summary, return_dict=True)

# Dynamically solve active scenario
s_row, df_sel_benefits = evaluate_portfolio_scenario(
    budget=scenario_params["budget"],
    equity_floor=scenario_params["equity_floor"],
    cost_case=scenario_params["cost_case"],
    cmf_case=scenario_params["cmf_case"],
    df_benefits=df_benefits,
)

is_official = (s_row["run_group"] == "OFFICIAL")
render_governance_header_banner(
    run_group=s_row["run_group"],
    is_official=is_official,
    scenario_params=scenario_params,
)

# -----------------------------------------------------------------------------
# Section 1 — Core Portfolio Metrics
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("1. Core portfolio metrics")

col1, col2, col3, col4 = st.columns(4)

total_corridors_count = len(df_master)
annual_ksi = df_sel_benefits["crashes_averted_ksi"].sum()

svi_mask = df_sel_benefits["equity_area_flag"] == True
high_svi_ksi = float(df_sel_benefits[svi_mask]["crashes_averted_ksi"].sum())
high_svi_ksi_share = (high_svi_ksi / annual_ksi * 100) if annual_ksi > 0 else 0.0

with col1:
    st.metric(
        "Estimated capital cost",
        format_currency_compact(s_row["selected_capital_cost"]),
        help=f"Planning-level estimate: {format_currency(s_row['selected_capital_cost'])} total initial construction cost for all shortlisted corridor projects.",
    )

with col2:
    st.metric(
        "Corridors funded",
        f"{int(s_row['selected_project_count'])} of {total_corridors_count}",
        help=f"Denominator: {total_corridors_count} candidate corridors in the network. Numerator: {int(s_row['selected_project_count'])} corridors selected for funding. Subject to engineering review.",
    )

with col3:
    st.metric(
        "Estimated KSI avoided / year",
        f"{format_ksi_compact(annual_ksi)} / yr",
        help=f"Denominator: {int(s_row['selected_project_count'])} funded corridors in this scenario. Severity scope: Fatal (K) + Serious injury (A) crashes. Planning-level estimate: ~{annual_ksi:,.1f} KSI avoided / yr.",
    )

with col4:
    st.metric(
        "High-SVI capital share",
        format_percent(s_row["achieved_equity_share"]),
        delta=f"Floor: {format_percent(s_row['equity_floor'])}",
        help=f"Denominator: Selected portfolio capital cost ({format_currency(s_row['selected_capital_cost'])}). Numerator: Capital allocated to high-SVI corridors. Measures capital spending input only; not proof of equitable safety outcomes. SVI is used as a spatial equity proxy.",
    )

# Secondary Metrics Expander
utilization_ratio = s_row["selected_capital_cost"] / s_row["budget_usd"] if s_row["budget_usd"] > 0 else 0.0
tot_ksi_2026 = df_master["annual_forecast_ksi_crashes_2026"].sum()
tot_averted = df_sel_benefits["crashes_averted_total"].sum()

with st.expander("Secondary metrics and economic indicators", expanded=False):
    sec1, sec2, sec3 = st.columns(3)
    with sec1:
        st.metric("Budget utilization", format_percent(utilization_ratio), help="Selected capital cost divided by planning budget ceiling.")
        st.metric("Estimated all-severity crashes avoided / year", f"{format_count_compact(tot_averted)} / yr", help=f"Denominator: {int(s_row['selected_project_count'])} funded corridors. Severity scope: All police-reported crash severities (K, A, B, C, O). Planning-level estimate: ~{tot_averted:,.1f} crashes avoided / yr.")
    with sec2:
        st.metric("Baseline KSI / year", f"{format_ksi_compact(tot_ksi_2026)} / yr", help=f"Denominator: Entire 43-corridor network. Severity scope: Calibrated 2026 pre-treatment baseline fatal (K) + serious injury (A) crashes (~{tot_ksi_2026:,.1f} KSI / yr).")
        st.metric("Total present value benefit", format_currency_compact(s_row["total_present_value_benefit"]), help=f"Planning-level estimate: {format_currency(s_row['total_present_value_benefit'])} comprehensive 20-year present value benefit.")
    with sec3:
        st.metric("Total net present benefit", format_currency_compact(s_row["total_net_present_benefit"]), help=f"Planning-level estimate: {format_currency(s_row['total_net_present_benefit'])} net present value benefit.")
        st.metric("Portfolio BCR (comprehensive)", format_bcr_compact(s_row["portfolio_bcr"]), help=f"Planning-level estimate: {s_row['portfolio_bcr']:,.1f} : 1 benefit-cost ratio from comprehensive crash costs.")
        st.metric("KSI benefit share in high-SVI areas", f"{high_svi_ksi_share:.1f}%", help=f"Denominator: Total annual KSI crashes avoided across funded corridors (~{annual_ksi:.1f}/yr). Numerator: Annual KSI avoided in high-SVI corridors (~{high_svi_ksi:.1f}/yr). SVI is used as a spatial equity proxy; it does not directly measure safety benefit equity.")

# -----------------------------------------------------------------------------
# Section 2 — 2026 Corridor Risk Forecast — Pre-Treatment Baseline
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("2. 2026 corridor risk forecast — pre-treatment baseline")
st.caption(
    "Modelled 2026 annual crash and KSI predictions for all 43 high-crash corridors before safety treatment. "
    "Demand risk rank is derived from the KSI forecast and serves as the baseline for treatment evaluation."
)

_funded_ids = set(df_sel_benefits["corridor_id"]) if not df_sel_benefits.empty else set()

df_forecast = df_master[[
    "corridor_id",
    "corridor_name",
    "demand_risk_rank_2026",
    "annual_forecast_total_crashes_2026",
    "annual_forecast_ksi_crashes_2026",
    "equity_classification_A_weighted_ge_0_75",
]].copy()

df_forecast["portfolio_status"] = df_forecast["corridor_id"].apply(
    lambda cid: "Funded" if cid in _funded_ids else "Deferred"
)
df_forecast["equity_classification_A_weighted_ge_0_75"] = df_forecast[
    "equity_classification_A_weighted_ge_0_75"
].apply(lambda v: "Yes" if v else "—")
df_forecast = df_forecast.sort_values("demand_risk_rank_2026")
df_forecast.columns = [
    "Corridor ID",
    "Corridor Name",
    "2026 Forecast Rank",
    "Predicted Total Crashes / Yr",
    "Predicted KSI / Yr",
    "High-SVI Equity Area",
    "Portfolio Status",
]

st.dataframe(
    df_forecast.style.format({
        "Predicted Total Crashes / Yr": "{:,.1f}",
        "Predicted KSI / Yr": "{:,.2f}",
    }),
    width="stretch",
    hide_index=True,
    height=340,
)

_net_total_2026 = float(df_master["annual_forecast_total_crashes_2026"].sum())
_net_ksi_2026 = float(df_master["annual_forecast_ksi_crashes_2026"].sum())
st.caption(
    f"Network total (all 43 corridors): ~{_net_total_2026:,.0f} predicted total crashes / yr · "
    f"~{_net_ksi_2026:.1f} predicted KSI / yr. Planning-level estimates; not official City projections."
)

# -----------------------------------------------------------------------------
# Section 3 — Funded Corridors — Benefit-Cost Efficiency
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("3. Funded corridors — benefit-cost efficiency")
st.caption(
    "Funded corridors ranked by individual Benefit-Cost Ratio (BCR). "
    "Evaluates estimated life-safety and economic return per dollar of initial construction investment."
)

df_eff = df_sel_benefits.copy()
df_eff["bcr_float"] = df_eff["benefit_cost_ratio"].astype(float)
df_eff = df_eff.sort_values("bcr_float", ascending=False)

# Top 15 decision-relevant corridors for readable display
df_top = df_eff.head(15).copy()

# High-SVI priority: #0D9488 (teal accent), Standard priority: #64748B (neutral slate)
bar_colors = ["#0D9488" if eq else "#64748B" for eq in df_top["equity_area_flag"]]

# Clean corridor label: ID + Name
corridor_labels = df_top["corridor_id"] + " " + df_top["corridor_name"]

fig_bcr = go.Figure()
fig_bcr.add_trace(go.Bar(
    y=corridor_labels,
    x=df_top["bcr_float"],
    orientation="h",
    marker_color=bar_colors,
    text=[f"{bcr:.1f}×" for bcr in df_top["bcr_float"]],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>BCR: %{x:.1f}×<extra></extra>",
))

fig_bcr.update_layout(
    height=480,
    margin=dict(l=10, r=50, t=10, b=10),
    xaxis=dict(title="Individual Project Benefit-Cost Ratio (BCR)", showgrid=True, gridcolor="#E2E8F0", tickfont=dict(color="#1E293B", size=11)),
    yaxis=dict(title="", tickfont=dict(size=11, color="#1E293B"), autorange="reversed"),
    font=dict(color="#1E293B"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)

legend_html = """
<div style="display:flex; align-items:center; gap:20px; font-size:12.5px; margin-top:6px; margin-bottom:8px; padding:6px 14px; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:6px; width:fit-content; box-shadow:0 1px 2px rgba(15,23,42,0.03);">
    <span style="font-weight:700; color:#0F172A;">Corridor Priority:</span>
    <span style="display:inline-flex; align-items:center; gap:7px;">
        <span style="width:13px; height:13px; background-color:#0D9488; border-radius:3px; display:inline-block;"></span>
        <span style="font-weight:500; color:#0F172A;">High-SVI Priority Corridor</span>
    </span>
    <span style="display:inline-flex; align-items:center; gap:7px;">
        <span style="width:13px; height:13px; background-color:#64748B; border-radius:3px; display:inline-block;"></span>
        <span style="font-weight:500; color:#0F172A;">Standard Priority Corridor</span>
    </span>
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)
st.plotly_chart(fig_bcr, width="stretch", config={"displayModeBar": False})

st.caption(
    "Note on interpretation: Bar length and numeric value indicate individual Benefit-Cost Ratio (BCR). "
    "Bar color represents spatial equity priority classification only (Teal = High-SVI Priority, Slate = Standard Priority), "
    "not relative performance or funding status."
)

top_count = len(df_top)
top_high_svi = int(df_top["equity_area_flag"].sum())
tot_funded = len(df_eff)
tot_high_svi = int(df_eff["equity_area_flag"].sum())

st.caption(
    f"Analytical takeaway: High-SVI priority corridors account for {top_high_svi} of the top {top_count} "
    f"benefit-cost investments (and {tot_high_svi} of the {tot_funded} funded corridors across the full portfolio). "
    f"Complete portfolio ranking of all {tot_funded} funded corridors is provided in the Selected Projects Detail Register below."
)

st.caption(
    "Methodological note: Portfolio selection is determined by the optimization model under budget, "
    "equity, treatment, and feasibility constraints—not by BCR ranking alone."
)

# Compact Equity Ledger by SVI Quartile
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
df_master_svi = df_master[["corridor_id", "corridor_length_weighted_svi"]].copy()
df_master_svi["svi_quartile"] = pd.qcut(
    df_master_svi["corridor_length_weighted_svi"],
    q=4,
    labels=[
        "Q1 — Lowest vulnerability",
        "Q2",
        "Q3",
        "Q4 — Highest vulnerability",
    ],
)
df_sel_svi = df_sel_benefits.merge(df_master_svi, on="corridor_id", how="left")
eq_ledger = (
    df_sel_svi.groupby("svi_quartile", observed=False)
    .agg(
        funded_projects=("corridor_id", "count"),
        capital_cost=("capital_project_cost", "sum"),
        ksi_avoided=("crashes_averted_ksi", "sum"),
    )
    .reset_index()
)
total_sel_cost = float(df_sel_benefits["capital_project_cost"].sum()) if not df_sel_benefits.empty else 1.0
eq_ledger["capital_share"] = (eq_ledger["capital_cost"] / total_sel_cost * 100)

df_ledger_display = pd.DataFrame({
    "SVI Quartile": eq_ledger["svi_quartile"],
    "Funded Corridors": eq_ledger["funded_projects"],
    "Capital Allocated": eq_ledger["capital_cost"].apply(format_currency),
    "Capital Share": eq_ledger["capital_share"].apply(lambda x: f"{x:.1f}%"),
    "Estimated KSI Avoided / Yr": eq_ledger["ksi_avoided"].apply(lambda x: f"~{x:.1f} / yr"),
})

with st.container():
    st.markdown("#### Equity ledger · SVI quartile")
    st.dataframe(df_ledger_display, width="stretch", hide_index=True)
    high_vuln_cost = float(eq_ledger.loc[eq_ledger["svi_quartile"].isin(["Q3", "Q4 — Highest vulnerability"]), "capital_cost"].sum())
    high_vuln_share = (high_vuln_cost / total_sel_cost * 100) if total_sel_cost > 0 else 0.0
    high_vuln_ksi = float(eq_ledger.loc[eq_ledger["svi_quartile"].isin(["Q3", "Q4 — Highest vulnerability"]), "ksi_avoided"].sum())
    st.caption(
        f"Analytical takeaway: Higher-vulnerability corridors (Q3 + Q4) receive {high_vuln_share:.1f}% of allocated capital "
        f"({format_currency(high_vuln_cost)}) and account for ~{high_vuln_ksi:.1f} annual KSI avoided, "
        f"substantially exceeding the portfolio equity floor objective."
    )
    st.caption(
        "Methodological distinction: SVI quartile distribution is a statistical analysis across the full 43-corridor network; "
        "the High-SVI policy classification is a binary spatial equity rule applied during optimization (SVI ≥ 0.75)."
    )

# -----------------------------------------------------------------------------
# Section 4 — Selected Projects Detail Register
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("4. Selected projects detail register")
st.caption(
    "Analytical planning portfolio; individual project engineering status is provisionally UNKNOWN (Engineering review required). "
    "Subject to engineering review and implementation approval."
)

df_table = df_sel_benefits[[
    "corridor_id",
    "corridor_name",
    "treatment_name",
    "capital_project_cost",
    "crashes_averted_total",
    "crashes_averted_k",
    "crashes_averted_a",
    "equity_area_flag",
    "physical_applicability_status",
]].copy()

df_table["equity_area_flag"] = df_table["equity_area_flag"].apply(format_equity_flag)
df_table["physical_applicability_status"] = df_table["physical_applicability_status"].apply(format_engineering_status)
df_table.columns = [
    "Corridor ID",
    "Corridor Name",
    "Recommended Treatment",
    "Estimated Capital Cost",
    "Estimated All-Severity Crashes Avoided / Yr",
    "Estimated Fatal (K) Avoided / Yr",
    "Estimated Serious Injury (A) Avoided / Yr",
    "High-SVI Priority Area",
    "Engineering Status",
]

st.dataframe(
    df_table.style.format({
        "Estimated Capital Cost": "${:,.0f}",
        "Estimated All-Severity Crashes Avoided / Yr": "{:,.2f}",
        "Estimated Fatal (K) Avoided / Yr": "{:,.2f}",
        "Estimated Serious Injury (A) Avoided / Yr": "{:,.2f}",
    }),
    width="stretch",
    hide_index=True,
    height=320,
)

# Standardized Consolidated Governance Footer
render_governance_footer()
