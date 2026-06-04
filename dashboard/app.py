"""
PriceHarvest – Agricultural Crop Price Intelligence System
Streamlit Interactive Dashboard

Run with:
    cd PriceHarvest/dashboard
    streamlit run app.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from src.preprocessing import load_all, combined
from src.features      import engineer_all
from src.insights      import (generate_dataset_insights,
                                generate_comparative_insights,
                                answer_analytical_questions,
                                _state_label)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PriceHarvest – Crop Price Intelligence",
    page_icon="🌾",
    layout="wide",
)

BG      = "#F8FAFC"
PALETTE = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED", "#0891B2"]

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.grid": True, "grid.color": "#E2E8F0",
    "font.family": "DejaVu Sans",
})

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .metric-card { background: #F1F5F9; border-radius: 12px; padding: 1rem; border-left: 4px solid #2563EB; }
    div[data-testid="metric-container"] { background: #F8FAFC; border-radius: 8px; padding: 0.5rem; border: 1px solid #E2E8F0; }
    .stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    dfs    = load_all()
    dfs_fe = {k: engineer_all(df) for k, df in dfs.items()}
    master = combined(dfs_fe)
    return dfs_fe, master


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🌾 PriceHarvest")
st.sidebar.caption("Agricultural Crop Price Intelligence")

page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "🔍 Crop Deep-Dive",
    "⚖️ Haryana vs Mumbai",
    "📈 Time Series",
    "💡 Insights & Q&A",
])

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Coverage**")
st.sidebar.info("📅 Jan 2023 – Dec 2025\n\n🗺️ Haryana & Maharashtra\n\n🌾 Wheat · Tomato · Onion")
st.sidebar.markdown("---")
st.sidebar.markdown("**Phase 1** · EDA & Dashboard")
st.sidebar.caption("Phase 2 → ML Forecasting (upcoming)")

with st.spinner("Loading data …"):
    dfs, master = load_data()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 – OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Overview":
    st.title("🌾 PriceHarvest – Agricultural Price Intelligence")
    st.markdown("**Analyzing 7,497 price records** across 3 crops × 2 states (2023–2025)")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records",      f"{len(master):,}")
    col2.metric("Haryana Wheat Avg",  "₹23.24/kg")
    col3.metric("Mumbai Wheat Avg",   "₹42.73/kg")
    col4.metric("Peak Price",         "₹120/kg", "Tomato Jul 2023")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Most Volatile",  "Tomato", "CV 71.8%")
    col6.metric("Most Stable",    "Wheat",  "CV 5.4%")
    col7.metric("Best Onion Month","November")
    col8.metric("Most Active Mkt","Karnal")

    st.markdown("---")
    st.subheader("📊 Average Price by Crop & State")

    df = master.copy()
    df["State_label"] = df["State"].apply(_state_label)
    df["Crop"] = df["Commodity"].str.title()
    summary = df.groupby(["Crop", "State_label"])["modal_price_kg"].mean().unstack("State_label")

    fig, ax = plt.subplots(figsize=(10, 5))
    summary.plot(kind="bar", ax=ax, color=["#2563EB", "#DC2626"], alpha=0.85,
                 edgecolor="white", width=0.65)
    ax.set_xlabel("Crop", fontsize=12)
    ax.set_ylabel("Average Modal Price (₹/kg)", fontsize=12)
    ax.set_title("Average Price by Crop & State (₹/kg)", fontweight="bold", fontsize=13)
    ax.legend(title="State", fontsize=11)
    plt.xticks(rotation=0)
    for container in ax.containers:
        ax.bar_label(container, fmt="₹%.2f", padding=3, fontsize=9)
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.subheader("📋 Dataset Summary")
    summary_table = (
        df.groupby(["Crop", "State_label"])["modal_price_kg"]
        .agg(Count="count", Mean="mean", Median="median", Std="std", Min="min", Max="max")
        .round(2).reset_index()
    )
    summary_table.columns = ["Crop", "State", "Records", "Mean ₹/kg", "Median ₹/kg",
                               "Std Dev", "Min ₹/kg", "Max ₹/kg"]
    st.dataframe(summary_table, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 – CROP DEEP-DIVE
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔍 Crop Deep-Dive":
    st.title("🔍 Individual Crop Analysis")

    c1, c2, c3 = st.columns(3)
    crop  = c1.selectbox("Crop",  ["Wheat", "Tomato", "Onion"])
    state = c2.selectbox("State", ["Haryana", "Mumbai"])
    key   = f"{'haryana' if state == 'Haryana' else 'mumbai'}_{crop.lower()}"
    df    = dfs[key]

    min_d = df["Arrival_Date"].min().date()
    max_d = df["Arrival_Date"].max().date()
    date_range = st.slider("Date Range", min_value=min_d, max_value=max_d,
                           value=(min_d, max_d), format="MMM YYYY")
    df = df[(df["Arrival_Date"].dt.date >= date_range[0]) &
            (df["Arrival_Date"].dt.date <= date_range[1])]

    markets    = ["All"] + sorted(df["Market"].unique().tolist())
    market_sel = c3.selectbox("Market Filter", markets)
    if market_sel != "All":
        df = df[df["Market"] == market_sel]

    st.markdown(f"**{len(df):,} records** · Mean: **₹{df['modal_price_kg'].mean():.2f}/kg** · "
                f"Min: **₹{df['modal_price_kg'].min():.2f}** · Max: **₹{df['modal_price_kg'].max():.2f}**")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution", "📅 Monthly Pattern", "📈 Price Trend", "🗓️ Heatmap"])

    with tab1:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
        prices = df["modal_price_kg"].dropna()
        ax1.hist(prices, bins=35, color="#2563EB", edgecolor="white", alpha=0.85)
        ax1.axvline(prices.mean(), color="#DC2626", lw=2, label=f"Mean ₹{prices.mean():.2f}")
        ax1.axvline(prices.median(), color="#16A34A", lw=2, ls="--", label=f"Median ₹{prices.median():.2f}")
        ax1.set_xlabel("Modal Price (₹/kg)"); ax1.set_ylabel("Frequency")
        ax1.set_title("Price Distribution"); ax1.legend()
        prices.plot.kde(ax=ax2, color="#2563EB", linewidth=2.5)
        ax2.set_xlabel("Modal Price (₹/kg)"); ax2.set_title("Price Density Curve")
        fig.suptitle(f"{crop} – {state}", fontweight="bold")
        st.pyplot(fig); plt.close()

    with tab2:
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        available   = [m for m in month_order if m in df["month_name"].values]
        data = [df[df["month_name"] == m]["modal_price_kg"].dropna().values for m in available]
        fig, ax = plt.subplots(figsize=(13, 5))
        bp = ax.boxplot(data, patch_artist=True, labels=available,
                        medianprops=dict(color="#DC2626", linewidth=2))
        colors = plt.cm.Blues(np.linspace(0.35, 0.85, len(available)))
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
        ax.set_ylabel("Modal Price (₹/kg)")
        ax.set_title(f"{crop} Monthly Price Box Plot – {state}", fontweight="bold")
        st.pyplot(fig); plt.close()

    with tab3:
        ts   = df.groupby("Arrival_Date")["modal_price_kg"].mean().sort_index()
        roll = ts.rolling(30, min_periods=1).mean()
        fig, ax = plt.subplots(figsize=(13, 4))
        ax.plot(ts.index, ts.values, alpha=0.3, color="#2563EB", lw=0.8, label="Daily")
        ax.plot(roll.index, roll.values, color="#2563EB", lw=2.5, label="30-day MA")
        ax.fill_between(ts.index, ts.values, alpha=0.07, color="#2563EB")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.xticks(rotation=30); ax.set_ylabel("₹/kg"); ax.legend()
        ax.set_title(f"{crop} Price Trend – {state}", fontweight="bold")
        st.pyplot(fig); plt.close()

    with tab4:
        pivot = df.groupby(["year", "month"])["modal_price_kg"].mean().unstack(level=1)
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        pivot.columns = [month_names[m - 1] for m in pivot.columns]
        fig, ax = plt.subplots(figsize=(12, max(3, len(pivot) + 1)))
        sns.heatmap(pivot, ax=ax, cmap="YlOrRd", annot=True, fmt=".1f",
                    cbar_kws={"label": "₹/kg"}, linewidths=0.5)
        ax.set_title(f"{crop} – Seasonal Heatmap (Year × Month) – {state}", fontweight="bold")
        st.pyplot(fig); plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 – MARKET COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
elif page == "⚖️ Haryana vs Mumbai":
    st.title("⚖️ Haryana vs Mumbai – Market Comparison")

    df = master.copy()
    df["State_label"] = df["State"].apply(_state_label)
    df["Crop"] = df["Commodity"].str.title()

    crop = st.selectbox("Select Crop", ["Wheat", "Tomato", "Onion"])
    sub  = df[df["Crop"] == crop]

    tab1, tab2, tab3 = st.tabs(["📈 Price Trend", "📊 Distribution", "📉 Volatility Stats"])

    with tab1:
        fig, ax = plt.subplots(figsize=(14, 5))
        for state, color in [("Haryana", "#2563EB"), ("Mumbai", "#DC2626")]:
            ts = (sub[sub["State_label"] == state]
                  .groupby("Arrival_Date")["modal_price_kg"].mean()
                  .rolling(14, min_periods=1).mean())
            ax.plot(ts.index, ts.values, color=color, lw=2, label=state)
            ax.fill_between(ts.index, ts.values, alpha=0.08, color=color)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.xticks(rotation=30)
        ax.set_ylabel("₹/kg (14-day MA)")
        ax.set_title(f"{crop} – Price Trend Comparison", fontweight="bold")
        ax.legend(fontsize=11)
        st.pyplot(fig); plt.close()

    with tab2:
        fig, ax = plt.subplots(figsize=(10, 5))
        for state, color in [("Haryana", "#2563EB"), ("Mumbai", "#DC2626")]:
            vals = sub[sub["State_label"] == state]["modal_price_kg"].dropna()
            vals.plot.kde(ax=ax, label=state, color=color, linewidth=2.5)
        ax.set_xlabel("Modal Price (₹/kg)")
        ax.set_title(f"{crop} – Price Distribution Comparison", fontweight="bold")
        ax.legend(fontsize=11)
        st.pyplot(fig); plt.close()

    with tab3:
        vol = sub.groupby("State_label")["modal_price_kg"].agg(
            Count="count", Mean="mean", Median="median", Std="std", Min="min", Max="max")
        vol["CV %"] = (vol["Std"] / vol["Mean"] * 100).round(1)
        st.dataframe(vol.round(2), use_container_width=True)

        fig, ax = plt.subplots(figsize=(8, 4))
        states = list(vol.index)
        vals   = vol["CV %"].values
        bars   = ax.bar(states, vals, color=["#2563EB", "#DC2626"], alpha=0.85, edgecolor="white", width=0.4)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"{v:.1f}%", ha="center", va="bottom", fontweight="bold")
        ax.set_ylabel("Coefficient of Variation (%)")
        ax.set_title(f"{crop} – Price Volatility (CV%)", fontweight="bold")
        st.pyplot(fig); plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 – TIME SERIES
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📈 Time Series":
    st.title("📈 Time Series Analysis")

    c1, c2 = st.columns(2)
    crop  = c1.selectbox("Crop",  ["Wheat", "Tomato", "Onion"])
    state = c2.selectbox("State", ["Haryana", "Mumbai"])
    key   = f"{'haryana' if state == 'Haryana' else 'mumbai'}_{crop.lower()}"
    df    = dfs[key]

    ts = df.groupby("Arrival_Date")["modal_price_kg"].mean()
    ts = ts.asfreq("D").interpolate("linear").dropna()

    tab1, tab2, tab3 = st.tabs(["📊 Rolling Averages", "🔀 Decomposition", "🔭 Trend Forecast"])

    with tab1:
        st.markdown("Moving averages smooth out noise and reveal underlying price trends.")
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(ts.index, ts.values, alpha=0.25, color="#94A3B8", lw=0.8, label="Daily")
        for w, color, style in [(7,"#2563EB","-"),(14,"#16A34A","--"),(30,"#D97706",":")]:
            ax.plot(ts.rolling(w,min_periods=1).mean(), color=color, lw=2, ls=style, label=f"{w}d MA")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.xticks(rotation=30); ax.legend()
        ax.set_ylabel("₹/kg")
        ax.set_title(f"{crop} – {state} Moving Averages", fontweight="bold")
        st.pyplot(fig); plt.close()

    with tab2:
        st.markdown("Decomposition separates price into **trend**, **seasonal**, and **residual** components.")
        period   = 30
        trend    = ts.rolling(period, center=True, min_periods=1).mean()
        detrended = ts - trend
        seasonal_vals = [detrended.iloc[list(range(i, len(detrended), period))].mean()
                         for i in range(period)]
        seasonal = pd.Series(
            [seasonal_vals[i % period] for i in range(len(ts))], index=ts.index)
        residual = ts - trend - seasonal

        fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)
        for ax, s, label, color in zip(axes,
            [trend, seasonal, residual],
            ["Trend","Seasonal","Residual"],
            ["#2563EB","#D97706","#DC2626"]):
            ax.plot(s.index, s.values, color=color, lw=1.5)
            ax.set_ylabel(label); ax.fill_between(s.index, s.values, alpha=0.1, color=color)
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.xticks(rotation=30)
        st.pyplot(fig); plt.close()

    with tab3:
        st.markdown("A **simple linear trend** extrapolated 30 days forward. *Note: For Phase 2, ARIMA/Prophet will replace this.*")
        n    = len(ts)
        x    = np.arange(n)
        coef = np.polyfit(x, ts.values, 1)
        trend_line   = np.poly1d(coef)(x)
        horizon      = 30
        fut_dates    = pd.date_range(ts.index[-1] + pd.Timedelta("1D"), periods=horizon)
        forecast     = np.poly1d(coef)(np.arange(n, n + horizon))
        sigma        = (ts.values - trend_line).std()

        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(ts.index, ts.values, alpha=0.3, color="#94A3B8", lw=0.8, label="Observed")
        ax.plot(ts.index, trend_line, color="#2563EB", lw=2, ls="--", label="Linear Trend")
        ax.plot(fut_dates, forecast, color="#16A34A", lw=2.5, label="30-Day Forecast")
        ax.fill_between(fut_dates, forecast-sigma, forecast+sigma, alpha=0.2,
                        color="#16A34A", label="±1σ Band")
        ax.axvline(ts.index[-1], color="#64748B", ls=":", lw=1.5)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.xticks(rotation=30); ax.legend()
        ax.set_ylabel("₹/kg")
        ax.set_title(f"{crop} – {state}: Trend + Forecast", fontweight="bold")
        st.pyplot(fig); plt.close()
        st.info(f"📈 Slope: ₹{coef[0]*30:.2f}/month | Forecast range: "
                f"₹{forecast.min():.2f} – ₹{forecast.max():.2f}/kg")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 – INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "💡 Insights & Q&A":
    st.title("💡 Price Intelligence Insights")

    all_ins = [generate_dataset_insights(df, key) for key, df in dfs.items()]
    comp    = generate_comparative_insights(master, all_ins)
    qa      = answer_analytical_questions(master, all_ins)

    st.subheader("🔍 Comparative Intelligence")
    cols = st.columns(2)
    for i, line in enumerate(comp["narratives"]):
        cols[i % 2].success(f"→ {line}")

    st.markdown("---")
    st.subheader("❓ Analytical Q&A")
    for item in qa:
        with st.expander(f"❓ {item['question']}"):
            st.markdown(f"**Answer:** {item['answer']}")

    st.markdown("---")
    st.subheader("📊 Dataset-Level Insights")
    for ins in all_ins:
        with st.expander(f"🌾 {ins['commodity']} – {ins['state']} | "
                         f"Avg ₹{ins['mean_price']}/kg | CV {ins['volatility_cv']:.1f}%"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Mean Price",  f"₹{ins['mean_price']}/kg")
            col2.metric("Peak Price",  f"₹{ins['max_price']}/kg")
            col3.metric("Volatility",  f"{ins['volatility_cv']:.1f}% CV")
            for line in ins["narratives"]:
                st.markdown(f"• {line}")
