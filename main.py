"""
PriceHarvest – Agricultural Crop Price Intelligence System
MAIN PIPELINE ORCHESTRATOR

Run this file to execute the full analysis pipeline:
    python main.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from src.preprocessing import load_all, combined
from src.features      import engineer_all
from src.eda           import run_eda
from src.comparison    import run_comparison
from src.timeseries    import run_timeseries
from src.insights      import run_insights
from src.advanced_viz  import run_advanced


def main():
    t0 = time.time()
    print("\n" + "═" * 65)
    print("  🌾  PriceHarvest – Agricultural Crop Price Intelligence")
    print("  Phase 1: EDA + Time-Series + Dashboard")
    print("═" * 65 + "\n")

    # 1. Load & preprocess
    print("▶  Phase 1: Data Preprocessing")
    dfs = load_all()

    # 2. Feature engineering
    print("\n▶  Phase 2: Feature Engineering")
    dfs_fe = {k: engineer_all(df) for k, df in dfs.items()}
    master = combined(dfs_fe)
    print(f"   Master dataset: {master.shape[0]:,} rows × {master.shape[1]} columns")

    # 3. Individual EDA
    print("\n▶  Phase 3: Individual Crop EDA")
    eda_paths = []
    for key, df in dfs_fe.items():
        eda_paths += run_eda(df, key)
    print(f"   Generated {len(eda_paths)} EDA charts")

    # 4. State comparison
    print("\n▶  Phase 4: State Comparison Analysis")
    comp_paths = run_comparison(master)
    print(f"   Generated {len(comp_paths)} comparison charts")

    # 5. Time series
    print("\n▶  Phase 5: Time Series Analysis")
    ts_paths = []
    for key, df in dfs_fe.items():
        ts_paths += run_timeseries(df, key)
    print(f"   Generated {len(ts_paths)} time-series charts")

    # 6. Insights
    print("\n▶  Phase 6: Price Intelligence Insights")
    all_ins, comp_ins, qa = run_insights(dfs_fe, master)

    # 7. Advanced visualizations
    print("\n▶  Phase 7: Advanced Visualizations")
    adv_paths = run_advanced(master)
    print(f"   Generated {len(adv_paths)} advanced charts")

    total_charts = len(eda_paths) + len(comp_paths) + len(ts_paths) + len(adv_paths)
    elapsed = time.time() - t0

    print("\n" + "─" * 65)
    print(f"  ✅  Pipeline complete in {elapsed:.1f}s")
    print(f"      Total charts : {total_charts}")
    print(f"      Insights     : outputs/insights/")
    print(f"      Charts       : outputs/charts/")
    print("─" * 65 + "\n")

    print("── Key Analytical Answers ─────────────────────────────────────────\n")
    for qa_item in qa:
        print(f"  Q: {qa_item['question']}")
        print(f"  A: {qa_item['answer']}\n")

    print("── Comparative Insights ────────────────────────────────────────────\n")
    for line in comp_ins["narratives"]:
        print(f"  → {line}")

    return dfs_fe, master, all_ins, comp_ins, qa


if __name__ == "__main__":
    main()
