"""Generate the presentation figures embedded in README.md.

Every figure in ``docs/figures/`` is produced by this script from committed
data only — no downloads, no private state, deterministic output:

* ``dashboard/streamlit/deployment_data/`` — production decision marts
  (corridor master, portfolio summary, project selections)
* ``docs/analysis_data/`` — curated analysis extracts
  (model comparison, 2026 corridor forecast)

Usage::

    python automation/generate_presentation_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dashboard" / "streamlit" / "deployment_data"
CURATED = ROOT / "docs" / "analysis_data"
OUT = ROOT / "docs" / "figures"

BASELINE_PORTFOLIO_ID = "PORT_OFF_BASE_B15M_EQ20"

# ---------------------------------------------------------------------------
# Visual identity
# ---------------------------------------------------------------------------
NAVY = "#0B2545"
BLUE = "#1565C0"
BLUE_LT = "#90CAF9"
RED = "#C62828"
GREEN = "#2E7D32"
AMBER = "#F9A825"
GRAY = "#90A4AE"
GRID = "#E3E8EC"
TEXT = "#37474F"
MUTED = "#607D8B"
LIGHT = "#CFD8DC"

ROAD_DIET = "Road Diet (4-to-3 Lane Conversion)"
PED_REFUGE = "Pedestrian Refuge Islands & Medians"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def style_axes(ax, grid_axis: str = "y") -> None:
    """Remove chartjunk: open frame, single light grid, no tick marks."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#B0BEC5")
    ax.tick_params(colors=TEXT, labelsize=9.5, length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=1.0)
        ax.set_axisbelow(True)


def add_header(fig, title: str, subtitle: str) -> None:
    fig.text(0.012, 0.975, title, fontsize=15.5, fontweight="bold", color=NAVY,
             ha="left", va="top", parse_math=False)
    fig.text(0.012, 0.905, subtitle, fontsize=9.8, color=MUTED,
             ha="left", va="top", parse_math=False)


def add_footer(fig) -> None:
    fig.text(
        0.985,
        0.012,
        "Vision Zero Chicago  ·  City of Chicago open data (2019–2025)  ·  "
        "planning estimates, not budget commitments",
        fontsize=7.6,
        color=GRAY,
        ha="right",
        va="bottom",
        parse_math=False,
    )


def save(fig, name: str) -> None:
    fig.savefig(OUT / name, dpi=170, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"saved  {name}")


def fmt_money(value: float) -> str:
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    return f"${value / 1_000:.0f}K"


def load_corridor_master() -> pd.DataFrame:
    return pd.read_csv(DATA / "corridor_master.csv")


def load_portfolio_summary() -> pd.DataFrame:
    return pd.read_csv(DATA / "portfolio_summary.csv")


# ---------------------------------------------------------------------------
# Figure 1 — Top corridors by forecast KSI burden
# ---------------------------------------------------------------------------
def figure_01_top_corridors() -> None:
    cm = load_corridor_master()
    top = (
        cm.sort_values("annual_forecast_ksi_crashes_2026", ascending=False)
        .head(15)
        .iloc[::-1]
    )

    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    y = range(len(top))
    bars = ax.barh(list(y), top["annual_forecast_ksi_crashes_2026"],
                   color=RED, height=0.72)
    ax.set_yticks(list(y),
                  [f"{name} ({cid})" for name, cid in
                   zip(top["corridor_name"], top["corridor_id"])],
                  fontsize=9.3, color=TEXT)
    style_axes(ax, grid_axis="x")
    ax.tick_params(axis="x", labelbottom=False)
    ax.set_xticks([])

    for bar, value in zip(bars, top["annual_forecast_ksi_crashes_2026"]):
        ax.text(
            value + 0.18,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            va="center",
            fontsize=9,
            color=TEXT,
            fontweight="bold",
        )

    ax.set_xlim(0, top["annual_forecast_ksi_crashes_2026"].max() * 1.18)
    add_header(
        fig,
        "Where the risk concentrates",
        "Top 15 of 43 high-crash corridors — forecast fatal + serious-injury "
        "(KSI) crashes for 2026",
    )
    add_footer(fig)
    fig.subplots_adjust(top=0.80, bottom=0.06, left=0.235, right=0.97)
    save(fig, "fig01_top_corridors_2026.png")


# ---------------------------------------------------------------------------
# Figure 2 — Risk vs vulnerability quadrant
# ---------------------------------------------------------------------------
def figure_02_risk_vulnerability() -> None:
    cm = load_corridor_master()
    x = cm["annual_forecast_total_crashes_2026"]
    y = cm["corridor_length_weighted_svi"] * 100.0
    size = 40 + cm["annual_forecast_ksi_crashes_2026"] * 26

    is_a = cm["equity_classification_A_weighted_ge_0_75"].astype(str).str.lower().eq("true")
    is_b = cm["equity_classification_B_share_ge_0_50"].astype(str).str.lower().eq("true")
    colors = [GREEN if a else (AMBER if b else GRAY) for a, b in zip(is_a, is_b)]

    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    ax.scatter(x, y, s=size, c=colors, alpha=0.85, edgecolor="white",
               linewidth=1.2, zorder=3)

    med_x, med_y = x.median(), y.median()
    ax.axvline(med_x, ls="--", lw=1.0, color=GRAY, zorder=1)
    ax.axhline(med_y, ls="--", lw=1.0, color=GRAY, zorder=1)
    ax.fill_between([med_x, x.max() * 1.04], med_y, 102,
                    color=RED, alpha=0.05, zorder=0)
    ax.text(
        x.max() * 1.02,
        101,
        "PRIORITY QUADRANT\nhigh burden + high vulnerability",
        color=RED,
        alpha=0.85,
        fontsize=8.5,
        fontweight="bold",
        ha="right",
        va="top",
    )

    annotated: set[str] = set()
    for _, row in cm.nlargest(4, "annual_forecast_total_crashes_2026").iterrows():
        ax.annotate(
            row["corridor_name"],
            (row["annual_forecast_total_crashes_2026"],
             row["corridor_length_weighted_svi"] * 100),
            xytext=(7, 6),
            textcoords="offset points",
            fontsize=8.5,
            color=TEXT,
        )
        annotated.add(row["corridor_id"])

    top_svi = cm[~cm["corridor_id"].isin(annotated)].nlargest(
        1, "corridor_length_weighted_svi"
    ).iloc[0]
    ax.annotate(
        f"{top_svi['corridor_name']} (highest vulnerability)",
        (top_svi["annual_forecast_total_crashes_2026"],
         top_svi["corridor_length_weighted_svi"] * 100),
        xytext=(7, 6),
        textcoords="offset points",
        fontsize=8.5,
        color=TEXT,
    )

    handles = [
        plt.Line2D([], [], marker="o", color="none", markerfacecolor=GREEN,
                   markeredgecolor="white", markersize=11,
                   label="Equity area A (SVI ≥ 0.75)"),
        plt.Line2D([], [], marker="o", color="none", markerfacecolor=AMBER,
                   markeredgecolor="white", markersize=11,
                   label="Equity area B (SVI share ≥ 0.50)"),
        plt.Line2D([], [], marker="o", color="none", markerfacecolor=GRAY,
                   markeredgecolor="white", markersize=11,
                   label="Not equity-designated"),
    ]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.30),
              ncol=3, frameon=False, fontsize=9)

    ax.set_xlabel("Forecast total crashes — 2026", fontsize=10, color=TEXT)
    ax.set_ylabel("Weighted social vulnerability index (0–100)", fontsize=10,
                  color=TEXT)
    ax.set_xlim(0, x.max() * 1.06)
    ax.set_ylim(0, 102)
    style_axes(ax)

    add_header(
        fig,
        "Risk × vulnerability: the priority quadrant",
        "Each bubble is one of the 43 high-crash corridors · size = forecast "
        "KSI crashes · dashed lines = medians",
    )
    add_footer(fig)
    fig.subplots_adjust(top=0.80, bottom=0.30, left=0.09, right=0.97)
    save(fig, "fig02_risk_vulnerability_quadrant.png")


# ---------------------------------------------------------------------------
# Figure 3 — Baseline portfolio allocation
# ---------------------------------------------------------------------------
def figure_03_portfolio_allocation() -> None:
    selections = pd.read_csv(DATA / "project_selections.csv")
    portfolio = selections[selections["portfolio_id"] == BASELINE_PORTFOLIO_ID]
    portfolio = portfolio.sort_values("capital_project_cost", ascending=False)
    top = portfolio.head(15).iloc[::-1]

    color_map = {ROAD_DIET: BLUE, PED_REFUGE: GREEN}
    bar_colors = [color_map.get(name, AMBER) for name in top["treatment_name"]]

    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    y = range(len(top))
    bars = ax.barh(list(y), top["capital_project_cost"] / 1_000_000,
                   color=bar_colors, height=0.72)
    ax.set_yticks(list(y),
                  [f"{name} ({cid})" for name, cid in
                   zip(top["corridor_name"], top["corridor_id"])],
                  fontsize=9.3, color=TEXT)
    style_axes(ax, grid_axis="x")
    ax.tick_params(axis="x", labelbottom=False)
    ax.set_xticks([])

    for bar, value in zip(bars, top["capital_project_cost"]):
        ax.text(
            bar.get_width() + 0.015,
            bar.get_y() + bar.get_height() / 2,
            fmt_money(value),
            va="center",
            fontsize=8.6,
            color=TEXT,
            fontweight="bold",
            parse_math=False,
        )

    top_share = top["capital_project_cost"].sum() / portfolio["capital_project_cost"].sum()
    road_diet_count = (portfolio["treatment_name"] == ROAD_DIET).sum()
    refuge_count = (portfolio["treatment_name"] == PED_REFUGE).sum()

    ax.set_xlim(0, top["capital_project_cost"].max() / 1_000_000 * 1.18)
    add_header(
        fig,
        "Where the $14.99M goes",
        f"Baseline portfolio · top 15 of 39 funded corridors "
        f"({top_share:.0%} of capital) · {road_diet_count} road diets + "
        f"{refuge_count} refuge projects",
    )
    add_footer(fig)
    fig.subplots_adjust(top=0.80, bottom=0.06, left=0.235, right=0.97)
    save(fig, "fig03_portfolio_allocation.png")


# ---------------------------------------------------------------------------
# Figure 4 — Budget sensitivity
# ---------------------------------------------------------------------------
def figure_04_budget_sensitivity() -> None:
    summary = load_portfolio_summary()
    official = summary[
        (summary["run_group"] == "OFFICIAL")
        & (summary["uncertainty_scenario"] == "BASE")
        & (summary["equity_floor"].round(2) == 0.20)
    ].sort_values("budget_usd")

    budgets_m = official["budget_usd"] / 1_000_000
    allocated_m = official["selected_capital_cost"] / 1_000_000

    fig, ax = plt.subplots(figsize=(10.2, 5.9))
    positions = range(len(official))
    width = 0.36
    ax.bar([p - width / 2 for p in positions], budgets_m, width,
           color=LIGHT, label="Budget ceiling")
    bars = ax.bar([p + width / 2 for p in positions], allocated_m, width,
                  color=BLUE, label="Capital allocated")

    for bar, row in zip(bars, official.itertuples()):
        y_anchor = max(row.budget_usd, row.selected_capital_cost) / 1e6 + 1.2
        ax.annotate(
            f"${row.selected_capital_cost / 1e6:.2f}M\n"
            f"{row.budget_utilization_pct:.1f}% used\n"
            f"{row.selected_corridor_count} of 43 corridors",
            (bar.get_x() + bar.get_width() / 2, y_anchor),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color=TEXT,
            fontweight="bold",
            parse_math=False,
        )

    ax.set_xticks(list(positions),
                  [f"${b:.0f}M ceiling" for b in budgets_m], fontsize=10)
    ax.set_ylabel("$ millions", fontsize=10, color=TEXT)
    ax.set_ylim(0, budgets_m.max() * 1.30)
    style_axes(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=9)

    add_header(
        fig,
        "Does the budget bind?",
        "Official BASE scenarios · 20% equity floor · the $15M ceiling binds "
        "(99.9% used); $25M+ funds all 43 corridors",
    )
    add_footer(fig)
    fig.subplots_adjust(top=0.80, bottom=0.14, left=0.09, right=0.97)
    save(fig, "fig04_budget_sensitivity.png")


# ---------------------------------------------------------------------------
# Figure 5 — Equity delivery vs required floor
# ---------------------------------------------------------------------------
def figure_05_equity_delivery() -> None:
    summary = load_portfolio_summary()
    official = summary[
        (summary["run_group"] == "OFFICIAL")
        & (summary["uncertainty_scenario"] == "BASE")
        & (summary["budget_usd"] == 15_000_000)
    ].sort_values("equity_floor")

    floors = (official["equity_floor"] * 100).tolist()
    achieved = (official["achieved_equity_share"] * 100).tolist()

    fig, ax = plt.subplots(figsize=(10.2, 5.9))
    positions = range(len(official))
    width = 0.36
    ax.bar([p - width / 2 for p in positions], floors, width, color=LIGHT,
           label="Required floor")
    bars = ax.bar([p + width / 2 for p in positions], achieved, width,
                  color=GREEN, label="Achieved share of capital")

    for bar, value in zip(bars, achieved):
        ax.annotate(
            f"{value:.1f}%",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            color=GREEN,
            fontweight="bold",
        )

    ax.set_xticks(list(positions), [f"{f:.0f}% floor" for f in floors],
                  fontsize=10)
    ax.set_ylabel("Share of capital (%)", fontsize=10, color=TEXT)
    ax.set_ylim(0, 60)
    style_axes(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=9)

    add_header(
        fig,
        "Equity floors are over-delivered at every level",
        "Spend in high-vulnerability (SVI) communities vs required floor · "
        "$15M baseline budget · the equity constraint never binds",
    )
    add_footer(fig)
    fig.subplots_adjust(top=0.80, bottom=0.14, left=0.09, right=0.97)
    save(fig, "fig05_equity_delivery.png")


# ---------------------------------------------------------------------------
# Figure 6 — Model bake-off
# ---------------------------------------------------------------------------
PRETTY_MODELS = {
    "seasonal_naive_lag12": "Seasonal naive",
    "historical_rolling_mean_12": "Rolling mean (12m)",
    "poisson_regression": "Poisson GLM",
    "negative_binomial_glm": "Negative binomial GLM",
}


def figure_06_model_bakeoff() -> None:
    comparison = pd.read_csv(CURATED / "model_comparison.csv")

    target_titles = {
        "total_crashes": "Total crashes",
        "ksi_crashes": "KSI crashes (killed or seriously injured)",
    }

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.4))

    for ax, target in zip(axes, ["total_crashes", "ksi_crashes"]):
        data = comparison[comparison["target"] == target].sort_values(
            "val_poisson_deviance"
        )
        labels = data["model_name"].map(PRETTY_MODELS).tolist()
        winners = data["is_selected_winner"].astype(str).str.lower().eq("true").tolist()
        labels = [f"{label} ★" if win else label
                  for label, win in zip(labels, winners)]
        colors = [BLUE if win else "#B0BEC5" for win in winners]

        y = range(len(data))
        bars = ax.barh(list(y), data["val_poisson_deviance"], color=colors,
                       height=0.62)
        ax.set_yticks(list(y), labels, fontsize=9.2, color=TEXT)
        ax.invert_yaxis()

        for bar, value in zip(bars, data["val_poisson_deviance"]):
            ax.text(
                bar.get_width() + 0.03,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.2f}",
                va="center",
                fontsize=8.8,
                color=TEXT,
                fontweight="bold",
            )

        ax.set_title(target_titles[target], fontsize=10.5, color=NAVY,
                     fontweight="bold", loc="left", pad=8)
        ax.set_xlim(0, data["val_poisson_deviance"].max() * 1.22)
        ax.tick_params(axis="x", labelbottom=False)
        ax.set_xticks([])
        style_axes(ax, grid_axis="x")

    add_header(
        fig,
        "Model bake-off — four candidates, two targets",
        "Validation Poisson deviance across 516 corridor-months · lower is "
        "better · ★ = model selected for production",
    )
    add_footer(fig)
    fig.subplots_adjust(top=0.76, bottom=0.08, left=0.20, right=0.97, wspace=0.55)
    save(fig, "fig06_model_bakeoff.png")


# ---------------------------------------------------------------------------
# Figure 7 — Forecast vs empirical benchmark
# ---------------------------------------------------------------------------
def figure_07_forecast_calibration() -> None:
    forecast = pd.read_csv(CURATED / "corridor_forecast_2026_annual.csv")
    x = forecast["annual_ksi_forecast_calibrated"]
    y = forecast["eb_annual_historical_ksi_benchmark"]
    rho = forecast[["annual_ksi_forecast_calibrated",
                    "eb_annual_historical_ksi_benchmark"]].corr(
        method="spearman").iloc[0, 1]

    fig, ax = plt.subplots(figsize=(9.6, 6.0))
    limit = max(x.max(), y.max()) * 1.10
    ax.plot([0, limit], [0, limit], ls="--", lw=1.1, color=GRAY, zorder=1,
            label="1:1 agreement")
    ax.scatter(x, y, s=52, color=BLUE, alpha=0.85, edgecolor="white",
               linewidth=1.1, zorder=3)

    for _, row in forecast.nlargest(3, "eb_annual_historical_ksi_benchmark").iterrows():
        ax.annotate(
            row["corridor_name"],
            (row["annual_ksi_forecast_calibrated"],
             row["eb_annual_historical_ksi_benchmark"]),
            xytext=(8, 5),
            textcoords="offset points",
            fontsize=8.6,
            color=TEXT,
        )

    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_xlabel("Calibrated 2026 KSI forecast (crashes / year)", fontsize=10,
                  color=TEXT)
    ax.set_ylabel("Empirical Bayes historical benchmark (KSI / year)",
                  fontsize=10, color=TEXT)
    style_axes(ax, grid_axis="both")
    ax.legend(loc="upper left", frameon=False, fontsize=9)

    add_header(
        fig,
        "The forecast tracks historical risk concentration",
        f"Calibrated 2026 KSI forecast vs empirical Bayes benchmark across 43 "
        f"corridors · Spearman ρ = {rho:.3f} (near-perfect rank agreement)",
    )
    add_footer(fig)
    fig.subplots_adjust(top=0.80, bottom=0.13, left=0.10, right=0.97)
    save(fig, "fig07_forecast_calibration.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    figure_01_top_corridors()
    figure_02_risk_vulnerability()
    figure_03_portfolio_allocation()
    figure_04_budget_sensitivity()
    figure_05_equity_delivery()
    figure_06_model_bakeoff()
    figure_07_forecast_calibration()
    print(f"\nall figures written to {OUT}")


if __name__ == "__main__":
    main()
