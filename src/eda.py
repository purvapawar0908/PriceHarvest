"""
PriceHarvest – Agricultural Crop Price Intelligence System
Module 3: Individual Crop EDA & Visualizations
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

PALETTE    = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED", "#0891B2"]
BG_COLOR   = "#F8FAFC"
GRID_COLOR = "#E2E8F0"

plt.rcParams.update({
    "figure.facecolor":  BG_COLOR,
    "axes.facecolor":    BG_COLOR,
    "axes.edgecolor":    "#94A3B8",
    "axes.labelcolor":   "#1E293B",
    "axes.grid":         True,
    "grid.color":        GRID_COLOR,
    "grid.linewidth":    0.8,
    "xtick.color":       "#475569",
    "ytick.color":       "#475569",
    "text.color":        "#1E293B",
    "font.family":       "DejaVu Sans",
})


def _save(fig, name: str):
    path = os.path.join(CHARTS_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    return path


def plot_price_distribution(df: pd.DataFrame, key: str):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"Price Distribution – {key.replace('_', ' ').title()}", fontsize=15, fontweight="bold")
    prices = df["modal_price_kg"].dropna()

    ax = axes[0]
    ax.hist(prices, bins=40, color=PALETTE[0], edgecolor="white", linewidth=0.5, alpha=0.85)
    ax.axvline(prices.mean(),   color="#DC2626", lw=2, ls="--", label=f"Mean ₹{prices.mean():.2f}")
    ax.axvline(prices.median(), color="#16A34A", lw=2, ls=":",  label=f"Median ₹{prices.median():.2f}")
    ax.set_xlabel("Modal Price (₹/kg)")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Modal Prices")
    ax.legend()

    ax2 = axes[1]
    markets = df["Market"].value_counts().head(5).index
    for i, mkt in enumerate(markets):
        subset = df[df["Market"] == mkt]["modal_price_kg"].dropna()
        if len(subset) < 10:
            continue
        subset.plot.kde(ax=ax2, label=mkt[:25], color=PALETTE[i % len(PALETTE)], linewidth=2)
    ax2.set_xlabel("Modal Price (₹/kg)")
    ax2.set_title("Price Density by Top Markets")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    return _save(fig, f"{key}_01_price_distribution")


def plot_monthly_boxplot(df: pd.DataFrame, key: str):
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    available   = [m for m in month_order if m in df["month_name"].values]
    fig, ax = plt.subplots(figsize=(15, 6))
    data_by_month = [df[df["month_name"] == m]["modal_price_kg"].dropna().values for m in available]
    bp = ax.boxplot(data_by_month, patch_artist=True, notch=False,
                    medianprops=dict(color="#DC2626", linewidth=2.5))
    colors = plt.cm.Blues(np.linspace(0.35, 0.85, len(available)))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
    ax.set_xticklabels(available)
    ax.set_xlabel("Month")
    ax.set_ylabel("Modal Price (₹/kg)")
    ax.set_title(f"Monthly Price Distribution – {key.replace('_',' ').title()}", fontweight="bold")
    fig.tight_layout()
    return _save(fig, f"{key}_02_monthly_boxplot")


def plot_time_series(df: pd.DataFrame, key: str):
    ts = df.groupby("Arrival_Date")["modal_price_kg"].mean().reset_index().sort_values("Arrival_Date")
    ts["roll30"] = ts["modal_price_kg"].rolling(30, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(ts["Arrival_Date"], ts["modal_price_kg"],
            color=PALETTE[0], alpha=0.35, linewidth=0.8, label="Daily Avg")
    ax.plot(ts["Arrival_Date"], ts["roll30"],
            color=PALETTE[0], linewidth=2.5, label="30-Day Rolling Mean")
    ax.fill_between(ts["Arrival_Date"], ts["modal_price_kg"], alpha=0.07, color=PALETTE[0])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.set_ylabel("Modal Price (₹/kg)")
    ax.set_title(f"Price Trend Over Time – {key.replace('_',' ').title()}", fontweight="bold")
    ax.legend()
    fig.tight_layout()
    return _save(fig, f"{key}_03_time_series")


def plot_seasonal_heatmap(df: pd.DataFrame, key: str):
    pivot = df.groupby(["year", "month"])["modal_price_kg"].mean().unstack(level=1)
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot.columns = [month_names[m - 1] for m in pivot.columns]
    fig, ax = plt.subplots(figsize=(14, max(3, len(pivot) * 0.9 + 1)))
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", annot=True, fmt=".1f",
                linewidths=0.5, linecolor="#CBD5E1",
                cbar_kws={"label": "Avg Modal Price (₹/kg)"})
    ax.set_title(f"Seasonal Price Heatmap – {key.replace('_',' ').title()}", fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    fig.tight_layout()
    return _save(fig, f"{key}_04_seasonal_heatmap")


def plot_market_comparison(df: pd.DataFrame, key: str):
    mkt = df.groupby("Market")["modal_price_kg"].agg(["mean", "std"]).reset_index()
    mkt = mkt.sort_values("mean", ascending=True).tail(15)
    fig, ax = plt.subplots(figsize=(12, max(5, len(mkt) * 0.5)))
    bars = ax.barh(mkt["Market"], mkt["mean"], xerr=mkt["std"],
                   color=PALETTE[1], edgecolor="white", linewidth=0.5,
                   error_kw=dict(elinewidth=1.2, ecolor="#64748B", capsize=3), alpha=0.85)
    for bar, val in zip(bars, mkt["mean"]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"₹{val:.2f}", va="center", ha="left", fontsize=9)
    ax.set_xlabel("Average Modal Price (₹/kg)")
    ax.set_title(f"Average Price by Market – {key.replace('_',' ').title()}", fontweight="bold")
    fig.tight_layout()
    return _save(fig, f"{key}_05_market_comparison")


def plot_volatility(df: pd.DataFrame, key: str):
    vol = df.groupby(["year", "month"])["modal_price_kg"].std().reset_index()
    vol["date"] = pd.to_datetime(vol[["year", "month"]].assign(day=1))
    vol = vol.sort_values("date")
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(vol["date"], vol["modal_price_kg"], width=20,
           color=PALETTE[3], alpha=0.8, edgecolor="white")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.set_ylabel("Std Dev of Price (₹/kg)")
    ax.set_title(f"Monthly Price Volatility – {key.replace('_',' ').title()}", fontweight="bold")
    fig.tight_layout()
    return _save(fig, f"{key}_06_volatility")


def run_eda(df: pd.DataFrame, key: str) -> list:
    print(f"  [EDA] {key}")
    paths = []
    paths.append(plot_price_distribution(df, key))
    paths.append(plot_monthly_boxplot(df, key))
    paths.append(plot_time_series(df, key))
    paths.append(plot_seasonal_heatmap(df, key))
    paths.append(plot_market_comparison(df, key))
    paths.append(plot_volatility(df, key))
    return paths
