"""
PriceHarvest – Agricultural Crop Price Intelligence System
Module 4: State Comparison Analysis (Haryana vs Mumbai)
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

warnings.filterwarnings("ignore")

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

BG      = "#F8FAFC"
H_COLOR = "#2563EB"
M_COLOR = "#DC2626"
CROPS   = ["Wheat", "Tomato", "Onion"]

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.grid": True, "grid.color": "#E2E8F0",
})


def _save(fig, name: str) -> str:
    path = os.path.join(CHARTS_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return path


def plot_state_trend_comparison(master: pd.DataFrame) -> list:
    paths = []
    for crop in CROPS:
        sub = master[master["Commodity"].str.title() == crop]
        fig, ax = plt.subplots(figsize=(16, 5))
        for state, color, label in [
            ("Haryana",     H_COLOR, "Haryana"),
            ("Maharashtra", M_COLOR, "Mumbai/Maharashtra"),
        ]:
            ts = (sub[sub["State"].str.contains(state, case=False)]
                  .groupby("Arrival_Date")["modal_price_kg"].mean()
                  .rolling(14, min_periods=1).mean())
            if ts.empty:
                continue
            ax.plot(ts.index, ts.values, color=color, linewidth=2, label=label)
            ax.fill_between(ts.index, ts.values, alpha=0.08, color=color)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=30)
        ax.set_ylabel("Modal Price (₹/kg)")
        ax.set_title(f"{crop} – Price Trend: Haryana vs Mumbai", fontsize=14, fontweight="bold")
        ax.legend(fontsize=11)
        fig.tight_layout()
        paths.append(_save(fig, f"compare_{crop.lower()}_01_trend"))
    return paths


def plot_avg_price_comparison(master: pd.DataFrame) -> str:
    summary = master.groupby(["Commodity", "State"])["modal_price_kg"].mean().reset_index()
    summary["State_label"] = summary["State"].apply(
        lambda s: "Haryana" if "Haryana" in s else "Mumbai")
    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(CROPS))
    w = 0.35
    for i, (state_label, color) in enumerate([("Haryana", H_COLOR), ("Mumbai", M_COLOR)]):
        vals = []
        for crop in CROPS:
            row = summary[(summary["Commodity"].str.title() == crop) &
                          (summary["State_label"] == state_label)]
            vals.append(row["modal_price_kg"].values[0] if len(row) else 0)
        bars = ax.bar(x + i * w, vals, w, label=state_label, color=color, alpha=0.85, edgecolor="white")
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                    f"₹{v:.2f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x + w / 2)
    ax.set_xticklabels(CROPS, fontsize=12)
    ax.set_ylabel("Average Modal Price (₹/kg)")
    ax.set_title("Average Price Comparison: Haryana vs Mumbai", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    fig.tight_layout()
    return _save(fig, "compare_all_02_avg_price")


def plot_price_spread(master: pd.DataFrame) -> str:
    df = master.copy()
    df["State_label"] = df["State"].apply(lambda s: "Haryana" if "Haryana" in s else "Mumbai")
    df["Crop"] = df["Commodity"].str.title()
    fig, axes = plt.subplots(1, 3, figsize=(16, 6), sharey=False)
    fig.suptitle("Price Spread by State – Violin Plot", fontsize=14, fontweight="bold")
    for ax, crop in zip(axes, CROPS):
        sub = df[df["Crop"] == crop]
        groups = [sub[sub["State_label"] == s]["modal_price_kg"].dropna().values
                  for s in ["Haryana", "Mumbai"]]
        parts = ax.violinplot(groups, positions=[1, 2], showmedians=True, showextrema=True)
        for pc, color in zip(parts["bodies"], [H_COLOR, M_COLOR]):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        ax.set_xticks([1, 2])
        ax.set_xticklabels(["Haryana", "Mumbai"])
        ax.set_title(crop, fontsize=13)
        ax.set_ylabel("Modal Price (₹/kg)")
    fig.tight_layout()
    return _save(fig, "compare_all_03_price_spread")


def plot_seasonal_comparison(master: pd.DataFrame) -> str:
    df = master.copy()
    df["State_label"] = df["State"].apply(lambda s: "Haryana" if "Haryana" in s else "Mumbai")
    df["Crop"] = df["Commodity"].str.title()
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fig, axes = plt.subplots(2, 3, figsize=(18, 9))
    fig.suptitle("Seasonal Price Heatmap (Month × Crop × State)", fontsize=15, fontweight="bold")
    for col, crop in enumerate(CROPS):
        for row, state in enumerate(["Haryana", "Mumbai"]):
            ax = axes[row][col]
            sub = df[(df["Crop"] == crop) & (df["State_label"] == state)]
            if sub.empty:
                ax.set_visible(False)
                continue
            pivot = sub.groupby(["year", "month"])["modal_price_kg"].mean().unstack(level=1)
            pivot.columns = [month_names[m - 1] for m in pivot.columns]
            sns.heatmap(pivot, ax=ax, cmap="YlOrRd", annot=True, fmt=".1f",
                        linewidths=0.4, cbar_kws={"shrink": 0.8}, annot_kws={"size": 8})
            ax.set_title(f"{state} – {crop}", fontsize=11)
            ax.set_xlabel("")
    fig.tight_layout()
    return _save(fig, "compare_all_04_seasonal")


def plot_volatility_comparison(master: pd.DataFrame) -> str:
    df = master.copy()
    df["State_label"] = df["State"].apply(lambda s: "Haryana" if "Haryana" in s else "Mumbai")
    df["Crop"] = df["Commodity"].str.title()
    vol = (df.groupby(["State_label", "Crop"])["modal_price_kg"]
           .agg(std="std", mean="mean")
           .assign(cv=lambda x: (x["std"] / x["mean"]) * 100)
           .reset_index())
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(CROPS))
    w = 0.35
    for i, (state, color) in enumerate([("Haryana", H_COLOR), ("Mumbai", M_COLOR)]):
        vals = [vol[(vol["State_label"] == state) & (vol["Crop"] == c)]["cv"].values for c in CROPS]
        vals = [v[0] if len(v) else 0 for v in vals]
        bars = ax.bar(x + i * w, vals, w, label=state, color=color, alpha=0.85, edgecolor="white")
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    f"{v:.1f}%", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x + w / 2)
    ax.set_xticklabels(CROPS, fontsize=12)
    ax.set_ylabel("Coefficient of Variation (%)")
    ax.set_title("Price Volatility Comparison: Haryana vs Mumbai", fontsize=13, fontweight="bold")
    ax.legend()
    fig.tight_layout()
    return _save(fig, "compare_all_05_volatility")


def run_comparison(master: pd.DataFrame) -> list:
    print("  [Comparison] Running state comparison charts …")
    paths = []
    paths += plot_state_trend_comparison(master)
    paths.append(plot_avg_price_comparison(master))
    paths.append(plot_price_spread(master))
    paths.append(plot_seasonal_comparison(master))
    paths.append(plot_volatility_comparison(master))
    return paths
