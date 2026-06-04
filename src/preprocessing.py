"""
PriceHarvest – Agricultural Crop Price Intelligence System
Module 1: Data Preprocessing Pipeline
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

DATASETS = {
    "haryana_wheat":  "haryana_wheat.csv",
    "haryana_tomato": "haryana_tomato.csv",
    "haryana_onion":  "haryana_onion.csv",
    "mumbai_wheat":   "mumbai_wheat.csv",
    "mumbai_tomato":  "mumbai_tomato.csv",
    "mumbai_onion":   "mumbai_onion.csv",
}

SEASON_MAP = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3:  "Spring",  4: "Spring",  5: "Spring",
    6:  "Summer",  7: "Summer",  8: "Summer",
    9:  "Autumn", 10: "Autumn", 11: "Autumn",
}


def load_raw(key: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, DATASETS[key])
    df = pd.read_csv(path)
    df["_source_key"] = key
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Arrival_Date"])
    price_cols = ["Min_Price", "Max_Price", "Modal_Price"]
    df = df.dropna(subset=price_cols)
    df = df[(df["Modal_Price"] > 0)]

    for col in ["State", "District", "Market", "Commodity", "Variety", "Grade"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    # Price conversion: quintal → kg
    df["min_price_kg"]   = df["Min_Price"]   / 100
    df["max_price_kg"]   = df["Max_Price"]   / 100
    df["modal_price_kg"] = df["Modal_Price"] / 100

    df["year"]       = df["Arrival_Date"].dt.year
    df["month"]      = df["Arrival_Date"].dt.month
    df["month_name"] = df["Arrival_Date"].dt.strftime("%b")
    df["week"]       = df["Arrival_Date"].dt.isocalendar().week.astype(int)
    df["season"]     = df["month"].map(SEASON_MAP)

    df = df.sort_values("Arrival_Date").reset_index(drop=True)
    return df


def load_all() -> dict:
    cleaned = {}
    for key in DATASETS:
        raw = load_raw(key)
        cleaned[key] = clean(raw)
        print(f"  [✓] {key:20s}  rows={len(cleaned[key]):>5}  "
              f"date_range={cleaned[key]['Arrival_Date'].min().date()} → "
              f"{cleaned[key]['Arrival_Date'].max().date()}")
    return cleaned


def combined(dfs: dict) -> pd.DataFrame:
    return pd.concat(dfs.values(), ignore_index=True)
