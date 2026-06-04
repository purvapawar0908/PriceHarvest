"""
PriceHarvest – Agricultural Crop Price Intelligence System
Module 2: Feature Engineering
"""

import pandas as pd
import numpy as np


def add_price_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price_range_kg"] = df["max_price_kg"] - df["min_price_kg"]
    df["price_midpoint"] = (df["max_price_kg"] + df["min_price_kg"]) / 2
    df["spread_pct"]     = (df["price_range_kg"] / df["modal_price_kg"]).replace(
        [np.inf, -np.inf], np.nan) * 100
    return df


def add_rolling_features(df: pd.DataFrame, windows=(7, 14, 30)) -> pd.DataFrame:
    df = df.copy().sort_values("Arrival_Date")
    for w in windows:
        df[f"roll_mean_{w}d"] = (
            df.groupby("Market")["modal_price_kg"]
            .transform(lambda x: x.rolling(w, min_periods=1).mean())
        )
        df[f"roll_std_{w}d"] = (
            df.groupby("Market")["modal_price_kg"]
            .transform(lambda x: x.rolling(w, min_periods=1).std())
        )
    return df


def add_volatility_index(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    grp = df.groupby(["Market", "year", "month"])["modal_price_kg"]
    stats = grp.agg(mean="mean", std="std").reset_index()
    stats["volatility_index"] = (stats["std"] / stats["mean"]).replace([np.inf, -np.inf], np.nan)
    df = df.merge(stats[["Market", "year", "month", "volatility_index"]],
                  on=["Market", "year", "month"], how="left")
    return df


def add_monthly_avg(df: pd.DataFrame) -> pd.DataFrame:
    grp = df.groupby(["State", "Commodity", "year", "month"])["modal_price_kg"].mean().reset_index()
    grp.rename(columns={"modal_price_kg": "monthly_avg_price_kg"}, inplace=True)
    df = df.merge(grp, on=["State", "Commodity", "year", "month"], how="left")
    return df


def engineer_all(df: pd.DataFrame) -> pd.DataFrame:
    df = add_price_features(df)
    df = add_rolling_features(df)
    df = add_volatility_index(df)
    df = add_monthly_avg(df)
    return df
