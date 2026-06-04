"""
PriceHarvest – Agricultural Crop Price Intelligence System
Module 5: Time Series Analysis
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

warnings.filterwarnings("ignore")

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)
BG = "#F8FAFC"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.grid": True, "grid.color": "#E2E8F0",
})


def _save(fig, name: str) -> str:
    path = os.path.join(CHARTS_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return path


def _build_ts(df: pd.DataFrame) -> pd.Series:
    ts = df.groupby("Arrival_Date")["modal_price_kg"].mean()
    ts = ts.asfreq("D").interpolate("linear")
    return ts


def plot_rolling_averages(df: pd.DataFrame, key: str) -> str:
    ts = _build_ts(df)
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(ts.index, ts.values, color="#94A3B8", lw=0.8, alpha=0.5, label="Daily")
    for w, color in zip([7, 14, 30], ["#2563EB", "#16A34A", "#D97706"]):
        ax.plot(ts.rolling(w, min_periods=1).mean(), color=color, lw=2, label=f"{w}-day MA")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.set_ylabel("Modal Price (₹/kg)")
    ax.set_title(f"Moving Averages – {key.replace('_',' ').title()}", fontweight="bold")
    ax.legend()
    fig.tight_layout()
    return _save(fig, f"{key}_ts_01_rolling")


def plot_decomposition(df: pd.DataFrame, key: str) -> str:
    ts = _build_ts(df)
    period = 30
    trend    = ts.rolling(period, center=True, min_periods=1).mean()
    detrended = ts - trend
    seasonal_vals = []
    for i in range(period):
        idx = list(range(i, len(detrended), period))
        seasonal_vals.append(detrended.iloc[idx].mean() if idx else 0)
    seasonal = pd.Series(
        [seasonal_vals[i % period] for i in range(len(ts))], index=ts.index)
    residual = ts - trend - seasonal

    fig, axes = plt.subplots(4, 1, figsize=(16, 12), sharex=True)
    fig.suptitle(f"Price Decomposition – {key.replace('_',' ').title()}",
                 fontsize=15, fontweight="bold")
    for ax, series, label, color in zip(
        axes,
        [ts, trend, seasonal, residual],
        ["Observed", "Trend", "Seasonal", "Residual"],
        ["#2563EB", "#16A34A", "#D97706", "#DC2626"],
    ):
        ax.plot(series.index, series.values, color=color, lw=1.5)
        ax.set_ylabel(label, fontsize=10)
        ax.fill_between(series.index, series.values, alpha=0.1, color=color)
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    fig.tight_layout()
    return _save(fig, f"{key}_ts_02_decomposition")


def plot_autocorrelation(df: pd.DataFrame, key: str) -> str:
    ts = _build_ts(df).dropna()
    n  = len(ts)
    max_lag = min(60, n // 2)
    lags = range(1, max_lag + 1)
    acf  = [ts.autocorr(lag=l) for l in lags]
    conf = 1.96 / np.sqrt(n)
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(list(lags), acf, color="#2563EB", alpha=0.7, width=0.7)
    ax.axhline(conf,  color="#DC2626", ls="--", lw=1.2, label=f"95% CI ±{conf:.3f}")
    ax.axhline(-conf, color="#DC2626", ls="--", lw=1.2)
    ax.axhline(0,     color="#475569", lw=0.8)
    ax.set_xlabel("Lag (days)")
    ax.set_ylabel("Autocorrelation")
    ax.set_title(f"Autocorrelation – {key.replace('_',' ').title()}", fontweight="bold")
    ax.legend()
    fig.tight_layout()
    return _save(fig, f"{key}_ts_03_acf")


def plot_forecast(df: pd.DataFrame, key: str) -> str:
    ts = _build_ts(df).dropna()
    n  = len(ts)
    x    = np.arange(n)
    coef = np.polyfit(x, ts.values, 1)
    trend_line = np.poly1d(coef)(x)
    horizon     = 30
    x_fut       = np.arange(n, n + horizon)
    future_dates = pd.date_range(ts.index[-1] + pd.Timedelta("1D"), periods=horizon)
    forecast    = np.poly1d(coef)(x_fut)
    resid = ts.values - trend_line
    sigma = resid.std()

    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(ts.index, ts.values, color="#94A3B8", lw=0.9, alpha=0.6, label="Observed")
    ax.plot(ts.index, trend_line, color="#2563EB", lw=2, ls="--", label="Trend")
    ax.plot(future_dates, forecast, color="#16A34A", lw=2.5, label="30-Day Forecast")
    ax.fill_between(future_dates, forecast - sigma, forecast + sigma,
                    alpha=0.2, color="#16A34A", label="±1σ band")
    ax.axvline(ts.index[-1], color="#64748B", ls=":", lw=1.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.set_ylabel("Modal Price (₹/kg)")
    ax.set_title(f"Trend + 30-Day Forecast – {key.replace('_',' ').title()}", fontweight="bold")
    ax.legend()
    fig.tight_layout()
    return _save(fig, f"{key}_ts_04_forecast")


def run_timeseries(df: pd.DataFrame, key: str) -> list:
    print(f"  [TimeSeries] {key}")
    paths = []
    paths.append(plot_rolling_averages(df, key))
    paths.append(plot_decomposition(df, key))
    paths.append(plot_autocorrelation(df, key))
    paths.append(plot_forecast(df, key))
    return paths
