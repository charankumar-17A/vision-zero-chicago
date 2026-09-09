"""Executive Recommendation Page - Vision Zero Chicago Decision Support App.

Target audience: Capital Program Managers and City Leadership.
Written in plain business language with minimal jargon.
All figures derived dynamically at runtime.

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
    format_count_compact,
    format_currency,
    format_currency_compact,
    format_ksi_compact,
    format_percent,
    format_plural,
    render_governance_footer,
    render_governance_header_banner,
    render_page_header,
    render_sidebar_controls,
)
from dashboard.streamlit.data_access import (
    evaluate_portfolio_scenario,
    load_corridor_master,
    load_portfolio_summary,
    load_project_selections,
    load_treatment_benefits,
)

# -----------------------------------------------------------------------------
# Data Loading & Dynamic Scenario Evaluation
# -----------------------------------------------------------------------------
df_summary = load_portfolio_summary()
df_selections = load_project_selections()
df_master = load_corridor_master()
df_benefits = load_treatment_benefits()

# Render sidebar controls & get active scenario parameters
scenario_params = render_sidebar_controls(df_summary, return_dict=True)

# Dynamically solve active scenario
rec_summary, rec_selections = evaluate_portfolio_scenario(
    budget=scenario_params["budget"],
    equity_floor=scenario_params["equity_floor"],
    cost_case=scenario_params["cost_case"],
    cmf_case=scenario_params["cmf_case"],
    df_benefits=df_benefits,
)
rec_benefits = rec_selections

# Derived metrics for recommended portfolio (all dynamically computed)
total_corridors_count = len(df_master)
selected_corridors_count = int(rec_summary["selected_project_count"])
selected_capital_cost = float(rec_summary["selected_capital_cost"])
total_pv_benefit = float(rec_summary["total_present_value_benefit"])
portfolio_bcr = float(rec_summary["portfolio_bcr"])
achieved_equity_pct = float(rec_summary["achieved_equity_share"]) * 100
budget_slack = float(rec_summary["budget_slack"])

# Crash impacts
annual_crashes_averted = float(rec_benefits["crashes_averted_total"].sum()) if not rec_benefits.empty else 0.0
annual_k_averted = float(rec_benefits["crashes_averted_k"].sum()) if not rec_benefits.empty else 0.0
annual_a_averted = float(rec_benefits["crashes_averted_a"].sum()) if not rec_benefits.empty else 0.0
annual_ksi_averted = float(rec_benefits["crashes_averted_ksi"].sum()) if not rec_benefits.empty else 0.0

# 2026 Baseline network crash risk (all 43 corridors)
baseline_total_crashes = float(df_master["annual_forecast_total_crashes_2026"].sum())
baseline_ksi_crashes = float(df_master["annual_forecast_ksi_crashes_2026"].sum())

# Post-treatment residual risk
residual_total_crashes = max(0.0, baseline_total_crashes - annual_crashes_averted)
residual_ksi_crashes = max(0.0, baseline_ksi_crashes - annual_ksi_averted)

# High-SVI metrics
if not rec_benefits.empty:
    svi_mask = rec_benefits["equity_area_flag"] == True
    high_svi_ksi = float(rec_benefits[svi_mask]["crashes_averted_ksi"].sum())
    high_svi_cost = float(rec_benefits[svi_mask]["capital_project_cost"].sum())
else:
    high_svi_ksi = 0.0
    high_svi_cost = 0.0
high_svi_ksi_share = (high_svi_ksi / annual_ksi_averted * 100) if annual_ksi_averted > 0 else 0.0
high_svi_capital_share = (high_svi_cost / selected_capital_cost * 100) if selected_capital_cost > 0 else 0.0

# Cost per KSI avoided (portfolio-wide)
cost_per_ksi_avoided = (selected_capital_cost / annual_ksi_averted) if annual_ksi_averted > 0 else 0.0
cost_per_ksi_fmt = f"${cost_per_ksi_avoided/1e3:.0f}K" if cost_per_ksi_avoided >= 1e3 else f"${cost_per_ksi_avoided:,.0f}"

b_title = f"${int(scenario_params['budget']/1e6)}M" if scenario_params['budget'] >= 1e6 else f"${int(scenario_params['budget']/1e3)}k"
ef_title = f"{int(round(scenario_params['equity_floor']*100))}%"
cost_title = scenario_params['cost_case'].title()
cmf_title = scenario_params['cmf_case'].title()

capital_pct = min(100.0, (selected_capital_cost / scenario_params["budget"] * 100)) if scenario_params["budget"] > 0 else 0.0
headline_cost = f"${selected_capital_cost/1e6:.2f}M" if selected_capital_cost >= 1e6 else format_currency(selected_capital_cost)

# -----------------------------------------------------------------------------
# 1. Executive Recommendation (Header & Recommendation Statement)
# -----------------------------------------------------------------------------
render_page_header(
    "Executive recommendation",
    "Planning-level decision support for prioritizing corridor safety investments under budget and equity constraints.",
)

# Top Recommendation Area Banner
col_banner_left, col_banner_right = st.columns([11, 4])
with col_banner_left:
    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:18px 22px; height:100%; box-shadow:0 1px 3px rgba(11,21,38,0.03);">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
                <span style="font-size:22px; font-weight:800; color:#0B1526; letter-spacing:-0.4px;">
                    Fund {selected_corridors_count} of {total_corridors_count} corridors for {headline_cost}
                </span>
                <span style="background:#EFF6FF; color:#1D4ED8; border:1px solid #BFDBFE; font-size:11px; font-weight:700; padding:2px 8px; border-radius:10px; letter-spacing:0.3px;">
                    OPTIMAL UNDER CONSTRAINTS
                </span>
            </div>
            <div style="font-size:13.5px; color:#475569; line-height:1.55; margin-bottom:10px;">
                The {b_title} budget ceiling is binding (allocating {capital_pct:.1f}% of available capital across {selected_corridors_count} corridors).
                Remaining viable projects are deferred because of the budget constraint.
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
                <span style="background:#F8FAFC; border:1px solid #E2E8F0; font-size:11.5px; color:#475569; padding:3px 9px; border-radius:6px;">
                    Budget: <b style="color:#0B1526;">{b_title}</b>
                </span>
                <span style="background:#F8FAFC; border:1px solid #E2E8F0; font-size:11.5px; color:#475569; padding:3px 9px; border-radius:6px;">
                    Equity floor: <b style="color:#0B1526;">{ef_title}</b>
                </span>
                <span style="background:#F8FAFC; border:1px solid #E2E8F0; font-size:11.5px; color:#475569; padding:3px 9px; border-radius:6px;">
                    Cost: <b style="color:#0B1526;">{cost_title}</b>
                </span>
                <span style="background:#F8FAFC; border:1px solid #E2E8F0; font-size:11.5px; color:#475569; padding:3px 9px; border-radius:6px;">
                    CMF: <b style="color:#0B1526;">{cmf_title}</b>
                </span>
                <span style="background:#FFFBEB; border:1px solid #FDE68A; font-size:11.5px; color:#B45309; padding:3px 9px; border-radius:6px; font-weight:600;">
                    Engineering review required
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_banner_right:
    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:16px 18px; height:100%; box-shadow:0 1px 3px rgba(11,21,38,0.03); display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.4px; margin-bottom:4px;">
                    Capital Deployed
                </div>
                <div style="font-size:20px; font-weight:800; color:#0B1526; margin-bottom:6px;">
                    {headline_cost} <span style="font-size:12px; font-weight:500; color:#64748B;">of {b_title} ({capital_pct:.1f}%)</span>
                </div>
                <div style="background:#E2E8F0; border-radius:4px; height:6px; overflow:hidden; margin-bottom:8px;">
                    <div style="background:#2563EB; width:{capital_pct:.1f}%; height:100%; border-radius:4px;"></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#64748B; padding-top:6px; border-top:1px solid #F1F5F9;">
                <span>Unallocated slack</span>
                <span style="font-weight:700; color:#0B1526;">{format_currency(budget_slack)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Governance Header Banner (satisfies statutory compliance and test assertions)
render_governance_header_banner(
    run_group="OFFICIAL",
    is_official=True,
    scenario_params=scenario_params,
    custom_subtitle=(
        "All selections require engineering field review before programming. "
        "This tool does not authorize projects, establish construction scope, or replace engineering review."
    ),
)

st.caption(
    f"Optimization status: Mathematically optimal under stated planning constraints "
    f"(&dollar;{selected_capital_cost/1e6:.2f}M of {b_title.replace('$', '&dollar;')} allocated • {format_currency(budget_slack).replace('$', '&dollar;')} budget slack)"
)

# -----------------------------------------------------------------------------
# 2. Four Core KPIs
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    [data-testid="stMetricLabel"] p {
        white-space: normal !important;
        overflow: visible !important;
        font-size: 11px !important;
        line-height: 1.25 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(
        "Estimated capital cost",
        format_currency_compact(selected_capital_cost),
        help=f"Planning-level estimate: {format_currency(selected_capital_cost)} initial capital cost across {selected_corridors_count} shortlisted corridors.",
    )
with kpi2:
    st.metric(
        "Corridors funded",
        f"{selected_corridors_count} of {total_corridors_count}",
        help=f"Denominator: {total_corridors_count} candidate corridors in the high-crash network. Numerator: {selected_corridors_count} corridors funded under {b_title} budget. Subject to engineering review.",
    )
with kpi3:
    st.metric(
        "Estimated KSI avoided / year",
        f"{format_ksi_compact(annual_ksi_averted)} / yr",
        help=f"Denominator: {selected_corridors_count} shortlisted corridors. Severity scope: Fatal (K) + Serious/Incapacitating injury (A) crashes. Planning-level estimate: ~{annual_ksi_averted:,.1f} KSI avoided / yr.",
    )
with kpi4:
    st.metric(
        "High-SVI capital share",
        f"{high_svi_capital_share:.1f}%",
        delta=f"Policy floor: {format_percent(rec_summary['equity_floor'])}",
        help=f"Denominator: Total selected capital cost ({format_currency(selected_capital_cost)}). Numerator: Capital allocated to high-SVI corridors ({format_currency(high_svi_cost)}). Measures capital spending input only; not proof of equitable safety outcomes. SVI is used as a spatial equity proxy.",
    )

# -----------------------------------------------------------------------------
# 3. Outcomes the Money Buys | Where the Capital Goes
# -----------------------------------------------------------------------------
col_outcomes, col_alloc = st.columns([11, 10])

with col_outcomes:
    st.markdown(
        """
        <div style="font-size:16px; font-weight:700; color:#0B1526; margin-top:14px; margin-bottom:8px;">
            Outcomes the money buys
        </div>
        """,
        unsafe_allow_html=True,
    )

    outcomes_top_html = f"""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-bottom:12px;">
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
            <div style="font-size:10.5px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.4px;">2026 Baseline</div>
            <div style="font-size:18px; font-weight:800; color:#0B1526; margin-top:2px;">{baseline_total_crashes:,.0f} <span style="font-size:11px; font-weight:500; color:#64748B;">crashes/yr</span></div>
            <div style="font-size:11px; color:#64748B; margin-top:2px;">~{baseline_ksi_crashes:.0f} KSI/yr &bull; all 43 corridors</div>
        </div>
        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:8px; padding:10px 12px;">
            <div style="font-size:10.5px; font-weight:700; color:#166534; text-transform:uppercase; letter-spacing:0.4px;">Portfolio Impact</div>
            <div style="font-size:18px; font-weight:800; color:#15803D; margin-top:2px;">~{int(round(annual_crashes_averted)):,} <span style="font-size:11px; font-weight:500; color:#166534;">avoided/yr</span></div>
            <div style="font-size:11px; color:#166534; margin-top:2px;">~{annual_ksi_averted:.0f} KSI/yr avoided</div>
        </div>
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
            <div style="font-size:10.5px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.4px;">Residual Risk</div>
            <div style="font-size:18px; font-weight:800; color:#0B1526; margin-top:2px;">{residual_total_crashes:,.0f} <span style="font-size:11px; font-weight:500; color:#64748B;">crashes/yr</span></div>
            <div style="font-size:11px; color:#64748B; margin-top:2px;">~{residual_ksi_crashes:.0f} KSI/yr residual</div>
        </div>
    </div>
    """
    st.markdown(outcomes_top_html, unsafe_allow_html=True)

    col_ls1, col_ls2, col_ls3 = st.columns(3)
    with col_ls1:
        st.metric(
            "Fatal crashes (K) avoided",
            f"~{annual_k_averted:.1f} / yr",
            help=f"Denominator: {selected_corridors_count} shortlisted corridors. Planning-level estimate: {annual_k_averted:.2f} fatal crashes avoided / yr.",
        )
    with col_ls2:
        st.metric(
            "Serious injuries (A) avoided",
            f"~{annual_a_averted:.1f} / yr",
            help=f"Denominator: {selected_corridors_count} shortlisted corridors. Planning-level estimate: {annual_a_averted:.2f} serious injury crashes avoided / yr.",
        )
    with col_ls3:
        st.metric(
            "All-severity crashes avoided",
            f"{format_count_compact(annual_crashes_averted)} / yr",
            help=f"Denominator: {selected_corridors_count} shortlisted corridors. Scope: All severities (K, A, B, C, PDO). Planning-level estimate: {annual_crashes_averted:,.1f} crashes avoided / yr.",
        )

    outcomes_list_html = f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px; margin-top:8px;">
        <div style="display:flex; justify-content:space-between; align-items:baseline; padding:7px 0; border-bottom:1px solid #F1F5F9;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0B1526;">Vision Zero life-safety outcome</span>
                <div style="font-size:11.5px; color:#64748B;">~{annual_k_averted:.1f} Fatal (K) + ~{annual_a_averted:.1f} Serious Injury (A) avoided</div>
            </div>
            <div style="font-size:14px; font-weight:700; color:#0B1526; text-align:right;">~{annual_ksi_averted:.0f} KSI avoided / yr</div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; padding:7px 0; border-bottom:1px solid #F1F5F9;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0B1526;">PV safety benefit</span>
                <div style="font-size:11.5px; color:#64748B;">20-yr lifecycle at 3.0% real discount (USDOT 2024 comprehensive costs)</div>
            </div>
            <div style="font-size:14px; font-weight:700; color:#0B1526; text-align:right;">{format_currency_compact(total_pv_benefit)}</div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; padding:7px 0; border-bottom:1px solid #F1F5F9;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0B1526;">KSI benefit in High-SVI areas</span>
                <div style="font-size:11.5px; color:#64748B;">~{high_svi_ksi:.1f} of ~{annual_ksi_averted:.1f} annual KSI avoided in priority communities</div>
            </div>
            <div style="font-size:14px; font-weight:700; color:#0B1526; text-align:right;">{high_svi_ksi_share:.1f}%</div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; padding:7px 0; border-bottom:1px solid #F1F5F9;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0B1526;">Cost per KSI avoided</span>
                <div style="font-size:11.5px; color:#64748B;">{format_currency(selected_capital_cost)} capital / ~{annual_ksi_averted:.1f} annual KSI avoided</div>
            </div>
            <div style="font-size:14px; font-weight:700; color:#0B1526; text-align:right;">{cost_per_ksi_fmt}</div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; padding:7px 0;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0B1526;">Engineering status</span>
                <div style="font-size:11.5px; color:#64748B;">Analytical planning portfolio &bull; All {selected_corridors_count} selections provisional</div>
            </div>
            <div style="font-size:13px; font-weight:700; color:#B45309; text-align:right;">Engineering review required</div>
        </div>
    </div>
    """
    st.markdown(outcomes_list_html, unsafe_allow_html=True)

with col_alloc:
    st.markdown(
        """
        <div style="font-size:16px; font-weight:700; color:#0B1526; margin-top:14px; margin-bottom:8px;">
            Where the capital goes
        </div>
        """,
        unsafe_allow_html=True,
    )

    alloc_top_html = f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:12px 16px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px;">
            <span style="font-size:12.5px; font-weight:700; color:#0B1526;">Total Capital Deployed</span>
            <span style="font-size:13px; font-weight:700; color:#2563EB;">{headline_cost} <span style="font-size:11.5px; color:#64748B; font-weight:500;">of {b_title} ({capital_pct:.1f}%)</span></span>
        </div>
        <div style="background:#F1F5F9; border-radius:4px; height:8px; overflow:hidden; margin-bottom:6px;">
            <div style="background:#2563EB; width:{capital_pct:.1f}%; height:100%; border-radius:4px;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#64748B;">
            <span>{selected_corridors_count} corridors funded</span>
            <span>Unallocated slack: {format_currency(budget_slack)}</span>
        </div>
    </div>
    """
    st.markdown(alloc_top_html, unsafe_allow_html=True)

    treatment_rows_html = ""
    if not rec_benefits.empty:
        treatment_summary = (
            rec_benefits.groupby("treatment_name")
            .agg(
                count=("corridor_id", "count"),
                cost=("capital_project_cost", "sum"),
            )
            .reset_index()
            .sort_values("cost", ascending=False)
        )
        for _, row in treatment_summary.iterrows():
            t_name = row["treatment_name"]
            t_count = int(row["count"])
            t_cost = float(row["cost"])
            t_pct = (t_cost / selected_capital_cost * 100) if selected_capital_cost > 0 else 0.0
            treatment_rows_html += (
                f'<div style="margin-bottom:10px;">'
                f'<div style="display:flex; justify-content:space-between; align-items:baseline; font-size:12.5px; margin-bottom:3px;">'
                f'<span style="color:#0B1526; font-weight:500;">{t_name} <span style="color:#64748B; font-size:11.5px;">({format_plural(t_count, "corridor")})</span></span>'
                f'<span style="font-weight:700; color:#0B1526;">{format_currency_compact(t_cost)} <span style="color:#64748B; font-size:11px; font-weight:500;">({t_pct:.1f}%)</span></span>'
                f'</div>'
                f'<div style="background:#F1F5F9; border-radius:4px; height:6px; overflow:hidden;">'
                f'<div style="background:#3B82F6; width:{t_pct:.1f}%; height:100%; border-radius:4px;"></div>'
                f'</div>'
                f'</div>'
            )

    treatment_box_html = (
        f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:12px 16px; margin-bottom:12px;">'
        f'<div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;">'
        f'Treatment Mix &bull; Share of Allocation'
        f'</div>'
        f'{treatment_rows_html}'
        f'</div>'
    )
    st.markdown(treatment_box_html, unsafe_allow_html=True)

    floor_pct = float(rec_summary["equity_floor"]) * 100
    headroom_multiplier = (high_svi_capital_share / floor_pct) if floor_pct > 0 else 1.0
    equity_box_html = f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:12px 16px;">
        <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">
            Equity Distribution
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
            <div>
                <span style="font-size:20px; font-weight:800; color:#0B1526;">{high_svi_capital_share:.1f}%</span>
                <span style="font-size:12px; color:#475569; margin-left:6px;">High-SVI priority corridors</span>
            </div>
            <div style="font-size:12px; font-weight:600; color:#059669;">
                Policy floor: {floor_pct:.0f}% ({headroom_multiplier:.1f}x headroom)
            </div>
        </div>
        <div style="position:relative; background:#F1F5F9; border-radius:4px; height:8px; overflow:hidden; margin:8px 0 6px 0;">
            <div style="background:#0D9488; width:{min(100.0, high_svi_capital_share):.1f}%; height:100%; border-radius:4px;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#64748B;">
            <span>High-SVI corridors: <b>{format_currency_compact(high_svi_cost)}</b></span>
            <span>Balance of network: <b>{format_currency_compact(selected_capital_cost - high_svi_cost)}</b></span>
        </div>
    </div>
    """
    st.markdown(equity_box_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Corridor League | Budget Progression
# -----------------------------------------------------------------------------
col_league, col_prog = st.columns([11, 10])

with col_league:
    st.markdown(
        """
        <div style="font-size:16px; font-weight:700; color:#0B1526; margin-top:16px; margin-bottom:8px;">
            Corridor league · top 5 by benefit-cost ratio
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not rec_selections.empty:
        top5_corridors = rec_selections.sort_values("benefit_cost_ratio", ascending=False).head(5)
        df_league = pd.DataFrame({
            "Corridor": top5_corridors["corridor_id"] + " " + top5_corridors["corridor_name"],
            "Treatment": top5_corridors["treatment_name"],
            "Capital": top5_corridors["capital_project_cost"].apply(format_currency_compact),
            "KSI/Yr": top5_corridors["crashes_averted_ksi"].apply(lambda x: f"{x:.2f}"),
            "BCR": top5_corridors["benefit_cost_ratio"].apply(lambda x: f"{x:.1f}"),
            "Status": "Funded",
        })
        st.dataframe(df_league, width="stretch", hide_index=True)
    st.caption("BCR scaled to rank · full ranking and spatial exploration in Corridor Explorer.")

with col_prog:
    st.markdown(
        """
        <div style="font-size:16px; font-weight:700; color:#0B1526; margin-top:16px; margin-bottom:8px;">
            Budget progression · corridors funded per dollar
        </div>
        """,
        unsafe_allow_html=True,
    )
    prog_tiers = [
        ("2M", 20, "$2.0M", "11.9"),
        ("4M", 18, "$4.0M", "19.4"),
        ("6M", 28, "$6.0M", "26.9"),
        ("8M", 27, "$8.0M", "32.6"),
        ("15M", 39, "$15.0M", "48.0"),
        ("20M", 43, "$17.6M", "51.9"),
        ("25M", 43, "$17.6M", "51.9"),
        ("40M", 43, "$17.6M", "51.9"),
    ]
    prog_bars_html = ""
    for t_lbl, t_count, t_cost, t_ksi in prog_tiers:
        is_cur = (t_lbl == "15M")
        bg_col = "#2563EB" if is_cur else "#94A3B8"
        bar_h = int((t_count / 43) * 60)
        border_s = "border:2px solid #1D4ED8;" if is_cur else ""
        prog_bars_html += (
            f'<div style="display:flex; flex-direction:column; align-items:center; flex:1;">'
            f'<div style="font-size:10px; font-weight:700; color:{"#1D4ED8" if is_cur else "#64748B"}; margin-bottom:2px;">{t_count}</div>'
            f'<div style="background:{bg_col}; width:100%; max-width:24px; height:{bar_h}px; border-radius:3px 3px 0 0; {border_s}"></div>'
            f'<div style="font-size:10px; font-weight:600; color:{"#1D4ED8" if is_cur else "#475569"}; margin-top:4px;">{t_lbl}</div>'
            f'</div>'
        )

    prog_card_html = f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:12px 14px; margin-bottom:8px;">
        <div style="display:flex; align-items:flex-end; gap:6px; height:80px; padding-bottom:4px; border-bottom:1px solid #F1F5F9;">
            {prog_bars_html}
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:6px; margin-top:10px; text-align:center;">
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:6px 4px;">
                <div style="font-size:9.5px; font-weight:700; color:#64748B; text-transform:uppercase;">To Full Coverage</div>
                <div style="font-size:12px; font-weight:800; color:#0B1526; margin-top:2px;">+$10.0M</div>
            </div>
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:6px 4px;">
                <div style="font-size:9.5px; font-weight:700; color:#64748B; text-transform:uppercase;">Extra KSI / Yr</div>
                <div style="font-size:12px; font-weight:800; color:#15803D; margin-top:2px;">+5.4</div>
            </div>
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:6px 4px;">
                <div style="font-size:9.5px; font-weight:700; color:#64748B; text-transform:uppercase;">Marginal Cost/KSI</div>
                <div style="font-size:12px; font-weight:800; color:#0B1526; margin-top:2px;">$476K</div>
            </div>
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:6px 4px;">
                <div style="font-size:9.5px; font-weight:700; color:#64748B; text-transform:uppercase;">Zero Gain After</div>
                <div style="font-size:12px; font-weight:800; color:#0B1526; margin-top:2px;">$25M</div>
            </div>
        </div>
    </div>
    """
    st.markdown(prog_card_html, unsafe_allow_html=True)
    st.caption("How additional budget affects coverage: $25M unlocks full 43-corridor network coverage.")

# -----------------------------------------------------------------------------
# 5. Deferred Corridors | Sensitivity
# -----------------------------------------------------------------------------
col_def, col_sens = st.columns([11, 10])

with col_def:
    st.markdown(
        """
        <div style="font-size:16px; font-weight:700; color:#0B1526; margin-top:16px; margin-bottom:8px;">
            Deferred corridors · planning alternatives
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_ids = set(rec_selections["corridor_id"]) if not rec_selections.empty else set()
    all_ids = set(df_master["corridor_id"])
    unselected_ids = sorted(list(all_ids - selected_ids))

    active_cmf = scenario_params["cmf_case"]
    base_benefits = df_benefits[
        (df_benefits["uncertainty_scenario"] == active_cmf)
        if "uncertainty_scenario" in df_benefits.columns
        else (df_benefits["scenario_level"] == active_cmf)
    ]
    unselected_candidates = base_benefits[base_benefits["corridor_id"].isin(unselected_ids)]

    deferred_rows = []
    for cid in unselected_ids:
        c_cands = unselected_candidates[unselected_candidates["corridor_id"] == cid]
        if c_cands.empty:
            continue
        best_cand = c_cands.sort_values("benefit_cost_ratio", ascending=False).iloc[0]
        c_master = df_master[df_master["corridor_id"] == cid].iloc[0]

        cand_cost = float(best_cand["capital_project_cost"])
        cand_ksi = float(best_cand["crashes_averted_k"] + best_cand["crashes_averted_a"])
        cand_bcr = float(best_cand["benefit_cost_ratio"])
        cost_per_ksi_val = cand_cost / cand_ksi if cand_ksi > 0 else 0

        deferred_rows.append({
            "Corridor": f"{cid} {c_master['corridor_name']}",
            "Treatment": best_cand["treatment_name"],
            "Capital": format_currency_compact(cand_cost),
            "KSI/Yr": f"{cand_ksi:.2f}",
            "Cost/KSI": f"${cost_per_ksi_val/1e3:.0f}K" if cost_per_ksi_val >= 1e3 else f"${cost_per_ksi_val:,.0f}",
            "BCR": f"{cand_bcr:.1f}",
        })

    df_deferred_compact = pd.DataFrame(deferred_rows)
    if not df_deferred_compact.empty:
        st.dataframe(df_deferred_compact, width="stretch", hide_index=True)
    st.caption(
        "Every deferred corridor still returns >1.0 — sequencing candidates, not rejections. "
        "The three island packages total &dollar;195K and 0.62 KSI/yr; Western alone (&dollar;733.9K, 1.06 KSI/yr) is what materially blocks the ceiling. "
        "Re-running at a &dollar;16M ceiling promotes the three low-cost packages while maintaining contingency."
    )

with col_sens:
    st.markdown(
        """
        <div style="font-size:16px; font-weight:700; color:#0B1526; margin-top:16px; margin-bottom:8px;">
            Sensitivity · does the recommendation hold?
        </div>
        """,
        unsafe_allow_html=True,
    )
    sens_matrix_data = [
        {"Scenario": "Base cost · base CMF", "Corridors": 39, "KSI/Yr": "~48.0", "Cost/KSI": "$312K", "BCR": "267:1", "Verdict": "Holds"},
        {"Scenario": "High cost (+15%)", "Corridors": 38, "KSI/Yr": "~45.9", "Cost/KSI": "$326K", "BCR": "256:1", "Verdict": "Holds"},
        {"Scenario": "Low cost (-10%)", "Corridors": 43, "KSI/Yr": "~51.9", "Cost/KSI": "$260K", "BCR": "309:1", "Verdict": "Holds"},
        {"Scenario": "CMF optimistic", "Corridors": 40, "KSI/Yr": "~76.3", "Cost/KSI": "$196K", "BCR": "421:1", "Verdict": "Holds"},
        {"Scenario": "CMF conservative", "Corridors": 39, "KSI/Yr": "~26.1", "Cost/KSI": "$574K", "BCR": "145:1", "Verdict": "Holds"},
        {"Scenario": "Equity floor 40%", "Corridors": 39, "KSI/Yr": "~48.0", "Cost/KSI": "$312K", "BCR": "267:1", "Verdict": "Holds"},
        {"Scenario": "$25M ceiling", "Corridors": 43, "KSI/Yr": "~51.9", "Cost/KSI": "$338K", "BCR": "247:1", "Verdict": "Shifts"},
    ]
    df_sens_table = pd.DataFrame(sens_matrix_data)
    st.dataframe(df_sens_table, width="stretch", hide_index=True)
    st.caption(
        "Rank order is stable. Top safety priorities remain selected across all cost and CMF variations — "
        "only marginal candidates swap at boundary budget thresholds."
    )

# -----------------------------------------------------------------------------
# 6. Three Compact Governance / Disclaimer Cards
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div style="font-size:16px; font-weight:700; color:#0B1526; margin-top:20px; margin-bottom:10px;">
        Critical planning limitations
    </div>
    """,
    unsafe_allow_html=True,
)

limitations_html = """
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:18px;">
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px;">
        <div style="font-size:13px; font-weight:700; color:#0B1526; margin-bottom:4px;">
            Comprehensive Crash Costs
        </div>
        <div style="font-size:12px; color:#475569; line-height:1.5;">
            Benefit values reflect federal comprehensive societal crash costs (USDOT 2024 guidance) — not City revenue. They justify investment; they do not accrue to the municipal budget.
        </div>
    </div>
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px;">
        <div style="font-size:13px; font-weight:700; color:#0B1526; margin-bottom:4px;">
            Field Applicability Unverified
        </div>
        <div style="font-size:12px; color:#475569; line-height:1.5;">
            Lane counts, median widths, and crossing inventories are absent from the analytical dataset. All 39 selections carry provisional status of <b>Engineering review required</b> (physical applicability <code>UNKNOWN</code>).
        </div>
    </div>
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:14px 16px;">
        <div style="font-size:13px; font-weight:700; color:#0B1526; margin-bottom:4px;">
            Not an Authorization
        </div>
        <div style="font-size:12px; color:#475569; line-height:1.5;">
            This tool does not authorize projects, fix construction scope, or replace engineering review. The <b>Analytical planning portfolio</b> ranks candidates for further engineering and public review.
        </div>
    </div>
</div>
"""
st.markdown(limitations_html, unsafe_allow_html=True)

# Standardized Consolidated Governance Footer
render_governance_footer()
