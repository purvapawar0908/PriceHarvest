"""
PriceHarvest – Agricultural Crop Price Intelligence System
Module 7: Advanced Professional Visualizations
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

warnings.filterwarnings("ignore")

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)
BG = "#F8FAFC"
PALETTE = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED", "#0891B2"]

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.grid": True, "grid.color": "#E2E8F0",
    "font.family": "DejaVu Sans",
})


def _save(fig, name: str) -> str:
    path = os.path.join(CHARTS_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return path


def plot_master_overview(master: pd.DataFrame) -> str:
    df = master.copy()
    df["State_label"] = df["State"].apply(lambda s: "Haryana" if "Haryana" in s else "Mumbai")
    df["Crop"] = df["Commodity"].str.title()
    summary = df.groupby(["Crop", "State_label"])["modal_price_kg"].agg(
        mean="mean", std="std").reset_index()

    fig, ax = plt.subplots(figsize=(12, 7))
    crops = ["Wheat", "Tomato", "Onion"]
    x = np.arange(len(crops))
    w = 0.35

    for i, (state, color) in enumerate(zip(["Haryana", "Mumbai"], ["#2563EB", "#DC2626"])):
        vals, errs = [], []
        for crop in crops:
            row = summary[(summary["Crop"] == crop) & (summary["State_label"] == state)]
            vals.append(row["mean"].values[0] if len(row) else 0)
            errs.append(row["std"].values[0] if len(row) else 0)
        bars = ax.bar(x + i * w, vals, w, label=state, color=color, alpha=0.85,
                      edgecolor="white", yerr=errs,
                      error_kw=dict(elinewidth=1.5, ecolor="#64748B", capsize=5))
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                    f"₹{v:.2f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_xticks(x + w / 2)
    ax.set_xticklabels(crops, fontsize=13)
    ax.set_ylabel("Average Modal Price (₹/kg)", fontsize=12)
    ax.set_title("PriceHarvest – Master Crop Price Overview\nHaryana vs Mumbai",
                 fontsize=15, fontweight="bold", pad=12)
    ax.legend(fontsize=12)
    fig.tight_layout()
    return _save(fig, "ADV_01_master_overview")


def plot_cross_crop_correlation(master: pd.DataFrame) -> str:
    df = master.copy()
    df["Crop_State"] = (df["Commodity"].str.title() + "_" +
                        df["State"].apply(lambda s: "HRY" if "Haryana" in s else "MUM"))
    pivot = (df.groupby(["Arrival_Date", "Crop_State"])["modal_price_kg"]
             .mean().unstack("Crop_State").resample("W").mean().dropna(how="all"))
    corr = pivot.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, ax=ax, cmap="coolwarm", vmin=-1, vmax=1,
                annot=True, fmt=".2f", linewidths=0.5,
                cbar_kws={"label": "Pearson Correlation"})
    ax.set_title("Cross-Crop Price Correlation (Weekly Avg)", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return _save(fig, "ADV_02_cross_correlation")


def plot_season_summary(master: pd.DataFrame) -> str:
    df = master.copy()
    df["Crop"] = df["Commodity"].str.title()
    season_order = ["Spring", "Summer", "Autumn", "Winter"]
    season_avg = df.groupby(["season", "Crop"])["modal_price_kg"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(13, 6))
    crops_list = ["Wheat", "Tomato", "Onion"]
    x = np.arange(len(season_order))
    w = 0.22

    for i, (crop, color) in enumerate(zip(crops_list, PALETTE)):
        vals = []
        for season in season_order:
            row = season_avg[(season_avg["season"] == season) & (season_avg["Crop"] == crop)]
            vals.append(row["modal_price_kg"].values[0] if len(row) else 0)
        bars = ax.bar(x + i * w, vals, w, label=crop, color=color, alpha=0.85, edgecolor="white")
        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                        f"₹{v:.1f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x + w)
    ax.set_xticklabels(season_order, fontsize=12)
    ax.set_ylabel("Average Price (₹/kg)")
    ax.set_title("Seasonal Price Patterns by Crop (All Markets Combined)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=11)
    fig.tight_layout()
    return _save(fig, "ADV_03_season_summary")


def plot_monthly_trend_overlay(master: pd.DataFrame) -> str:
    df = master.copy()
    df["State_label"] = df["State"].apply(lambda s: "Haryana" if "Haryana" in s else "Mumbai")
    df["Crop_State"]  = df["Commodity"].str.title() + " (" + df["State_label"] + ")"
    fig, ax = plt.subplots(figsize=(16, 7))
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for i, key in enumerate(df["Crop_State"].unique()):
        sub = df[df["Crop_State"] == key]
        monthly = sub.groupby("month")["modal_price_kg"].mean().reindex(range(1, 13))
        ax.plot(month_names, monthly.values, marker="o", linewidth=2.2,
                markersize=6, color=PALETTE[i % len(PALETTE)], label=key)
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Modal Price (₹/kg)")
    ax.set_title("Monthly Price Trend Overlay – All Crops & States", fontsize=14, fontweight="bold")
    ax.legend(fontsize=9, ncol=2)
    fig.tight_layout()
    return _save(fig, "ADV_04_monthly_overlay")


def plot_top_price_events(master: pd.DataFrame) -> str:
    df = master.copy()
    df["Label"] = (df["Commodity"].str.title() + " – " +
                   df["Market"].str[:20] + "\n" +
                   df["Arrival_Date"].dt.strftime("%d %b %Y"))
    top = df.nlargest(10, "modal_price_kg")
    fig, ax = plt.subplots(figsize=(13, 6))
    colors = [PALETTE[0] if "Wheat" in l else PALETTE[1] if "Tomato" in l else PALETTE[2]
              for l in top["Commodity"]]
    bars = ax.barh(range(len(top)), top["modal_price_kg"], color=colors, alpha=0.85, edgecolor="white")
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top["Label"], fontsize=9)
    for bar, v in zip(bars, top["modal_price_kg"]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                f"₹{v:.2f}/kg", va="center", fontsize=9)
    ax.set_xlabel("Modal Price (₹/kg)")
    ax.set_title("Top-10 Highest Price Events on Record", fontsize=13, fontweight="bold")
    legend_patches = [mpatches.Patch(color=PALETTE[0], label="Wheat"),
                      mpatches.Patch(color=PALETTE[1], label="Tomato"),
                      mpatches.Patch(color=PALETTE[2], label="Onion")]
    ax.legend(handles=legend_patches, fontsize=10)
    fig.tight_layout()
    return _save(fig, "ADV_05_top_price_events")


def run_advanced(master: pd.DataFrame) -> list:
    print("  [Advanced] Generating advanced visualizations …")
    paths = []
    paths.append(plot_master_overview(master))
    paths.append(plot_cross_crop_correlation(master))
    paths.append(plot_season_summary(master))
    paths.append(plot_monthly_trend_overlay(master))
    paths.append(plot_top_price_events(master))
    return paths
