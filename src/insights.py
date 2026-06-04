"""
PriceHarvest – Agricultural Crop Price Intelligence System
Module 6: Price Intelligence Insights Engine
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

INSIGHTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "insights")
os.makedirs(INSIGHTS_DIR, exist_ok=True)

MONTH_NAMES = {
    1:"January", 2:"February", 3:"March", 4:"April",
    5:"May", 6:"June", 7:"July", 8:"August",
    9:"September", 10:"October", 11:"November", 12:"December"
}


def _cv(series):
    m = series.mean()
    return (series.std() / m * 100) if m > 0 else np.nan


def _state_label(s):
    return "Haryana" if "Haryana" in str(s) else "Mumbai"


def _best_sell_months(df, top_n=3):
    mth = df.groupby("month")["modal_price_kg"].mean()
    return [MONTH_NAMES[m] for m in mth.nlargest(top_n).index.tolist()]


def _worst_sell_months(df, top_n=2):
    mth = df.groupby("month")["modal_price_kg"].mean()
    return [MONTH_NAMES[m] for m in mth.nsmallest(top_n).index.tolist()]


def generate_dataset_insights(df: pd.DataFrame, key: str) -> dict:
    commodity = df["Commodity"].iloc[0].title()
    state     = _state_label(df["State"].iloc[0])
    prices    = df["modal_price_kg"]
    monthly   = df.groupby("month")["modal_price_kg"].mean()
    best_market = df.groupby("Market")["modal_price_kg"].mean().idxmax()
    peak_price  = prices.max()
    peak_date   = df.loc[df["modal_price_kg"].idxmax(), "Arrival_Date"].strftime("%d %b %Y")
    volatility_cv = _cv(prices)
    stability = ("highly stable"     if volatility_cv < 10  else
                 "moderately stable" if volatility_cv < 25  else
                 "highly volatile")

    return {
        "key":              key,
        "commodity":        commodity,
        "state":            state,
        "mean_price":       round(prices.mean(), 2),
        "median_price":     round(prices.median(), 2),
        "max_price":        round(peak_price, 2),
        "min_price":        round(prices.min(), 2),
        "volatility_cv":    round(volatility_cv, 2),
        "stability_label":  stability,
        "best_sell_months": _best_sell_months(df),
        "worst_sell_months": _worst_sell_months(df),
        "best_market":      best_market,
        "peak_price_date":  peak_date,
        "narratives": [
            f"{commodity} prices in {state} average ₹{prices.mean():.2f}/kg (median ₹{prices.median():.2f}/kg).",
            f"Best months to sell {commodity} in {state}: {', '.join(_best_sell_months(df))}.",
            f"Avoid selling in {', '.join(_worst_sell_months(df))} — historically lowest prices.",
            f"Highest ever recorded price: ₹{peak_price:.2f}/kg on {peak_date}.",
            f"Price behaviour is {stability} (CV = {volatility_cv:.1f}%).",
            f"Market with highest average price: {best_market}.",
        ]
    }


def generate_comparative_insights(master: pd.DataFrame, all_insights: list) -> dict:
    master = master.copy()
    master["State_label"] = master["State"].apply(_state_label)
    master["Crop"]        = master["Commodity"].str.title()

    sorted_by_vol = sorted(all_insights, key=lambda x: x["volatility_cv"])
    most_stable   = sorted_by_vol[0]
    most_volatile = sorted_by_vol[-1]

    cheaper = {}
    for crop in ["Wheat", "Tomato", "Onion"]:
        sub = master[master["Crop"] == crop]
        state_avg = sub.groupby("State_label")["modal_price_kg"].mean()
        if len(state_avg) == 2:
            cheaper[crop] = state_avg.idxmin()

    best_markets = {}
    for crop in ["Wheat", "Tomato", "Onion"]:
        sub = master[master["Crop"] == crop]
        if not sub.empty:
            best_markets[crop] = sub.groupby("Market")["modal_price_kg"].mean().idxmax()

    narratives = [
        f"Most stable crop: {most_stable['commodity']} in {most_stable['state']} (CV = {most_stable['volatility_cv']:.1f}%).",
        f"Most volatile crop: {most_volatile['commodity']} in {most_volatile['state']} (CV = {most_volatile['volatility_cv']:.1f}%).",
    ]
    for crop, state in cheaper.items():
        other = "Mumbai" if state == "Haryana" else "Haryana"
        narratives.append(f"{crop} is cheaper in {state} compared to {other}.")
    for crop, mkt in best_markets.items():
        narratives.append(f"Highest average {crop} price market: {mkt}.")

    return {
        "most_stable":         most_stable,
        "most_volatile":       most_volatile,
        "cheaper_by_crop":     cheaper,
        "best_market_by_crop": best_markets,
        "narratives":          narratives,
    }


def answer_analytical_questions(master: pd.DataFrame, all_insights: list) -> list:
    master = master.copy()
    master["State_label"] = master["State"].apply(_state_label)
    master["Crop"]        = master["Commodity"].str.title()
    qa = []

    top_vol = max(all_insights, key=lambda x: x["volatility_cv"])
    qa.append({"question": "Which crop-state shows the highest price volatility?",
               "answer": f"{top_vol['commodity']} in {top_vol['state']} (CV = {top_vol['volatility_cv']:.1f}%)"})

    tom = master[master["Crop"] == "Tomato"]
    best_tom = tom.groupby(["State_label", "Market"])["modal_price_kg"].mean().idxmax()
    qa.append({"question": "Which market gives the highest average Tomato price?",
               "answer": f"{best_tom[1]} ({best_tom[0]})"})

    wheat = master[master["Crop"] == "Wheat"].groupby("State_label")["modal_price_kg"].mean()
    if len(wheat) == 2:
        qa.append({"question": "Which state has cheaper Wheat?",
                   "answer": f"{wheat.idxmin()} — avg ₹{wheat.min():.2f}/kg vs ₹{wheat.max():.2f}/kg"})

    onion = master[master["Crop"] == "Onion"]
    best_onion_month = MONTH_NAMES[int(onion.groupby("month")["modal_price_kg"].mean().idxmax())]
    qa.append({"question": "What is the best month to sell Onion (both states combined)?",
               "answer": best_onion_month})

    idx_max = master["modal_price_kg"].idxmax()
    row_max = master.loc[idx_max]
    qa.append({"question": "What is the highest single price ever recorded?",
               "answer": f"₹{row_max['modal_price_kg']:.2f}/kg — {row_max['Crop']} at {row_max['Market']} on {row_max['Arrival_Date'].strftime('%d %b %Y')}"})

    busiest = master.groupby("Market").size().idxmax()
    qa.append({"question": "Which market has the most price records (most active)?",
               "answer": busiest})
    return qa


def save_insights(all_insights, comparative, qa_list) -> str:
    bundle = {
        "generated_at":         datetime.now().isoformat(),
        "dataset_insights":     all_insights,
        "comparative_insights": comparative,
        "qa":                   qa_list,
    }
    json_path = os.path.join(INSIGHTS_DIR, "price_intelligence.json")
    with open(json_path, "w") as f:
        json.dump(bundle, f, indent=2, default=str)

    txt_path = os.path.join(INSIGHTS_DIR, "price_intelligence_report.txt")
    with open(txt_path, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("  PriceHarvest – Price Intelligence Report\n")
        f.write(f"  Generated: {datetime.now().strftime('%d %b %Y %H:%M')}\n")
        f.write("=" * 70 + "\n\n")
        f.write("── DATASET-LEVEL INSIGHTS ──────────────────────────────────────────\n\n")
        for ins in all_insights:
            f.write(f"▶  {ins['commodity'].upper()} – {ins['state'].upper()}\n")
            for line in ins["narratives"]:
                f.write(f"   • {line}\n")
            f.write("\n")
        f.write("── COMPARATIVE INSIGHTS ────────────────────────────────────────────\n\n")
        for line in comparative["narratives"]:
            f.write(f"  → {line}\n")
        f.write("\n── ANALYTICAL Q&A ──────────────────────────────────────────────────\n\n")
        for qa in qa_list:
            f.write(f"  Q: {qa['question']}\n  A: {qa['answer']}\n\n")
    return txt_path


def run_insights(dfs: dict, master: pd.DataFrame):
    print("  [Insights] Generating intelligence report …")
    all_ins = [generate_dataset_insights(df, key) for key, df in dfs.items()]
    comp    = generate_comparative_insights(master, all_ins)
    qa      = answer_analytical_questions(master, all_ins)
    path    = save_insights(all_ins, comp, qa)
    print(f"  [Insights] Report saved → {path}")
    return all_ins, comp, qa
