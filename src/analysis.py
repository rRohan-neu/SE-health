"""Reusable analytical helpers for downloaded Statistics Canada tables."""
import pandas as pd

def latest_reference_period(df: pd.DataFrame) -> pd.DataFrame:
    if "REF_DATE" not in df.columns:
        raise ValueError("REF_DATE column is required")
    periods = pd.to_numeric(df["REF_DATE"].astype(str).str[:4], errors="coerce")
    if periods.notna().sum() == 0:
        raise ValueError("No interpretable reference years found")
    return df.loc[periods.eq(periods.max())].copy()

def summarize_dimension(df: pd.DataFrame, dimension: str, value_col: str = "VALUE") -> pd.DataFrame:
    if dimension not in df.columns or value_col not in df.columns:
        raise ValueError(f"Required columns missing: {dimension}, {value_col}")
    work = df.copy()
    work[value_col] = pd.to_numeric(work[value_col], errors="coerce")
    return (work.groupby(dimension, dropna=False)[value_col]
            .agg(mean="mean", median="median", observations="count")
            .reset_index())

def rank_sensitivity(profiles: list, weight_sets: list[dict]) -> pd.DataFrame:
    """Re-score profiles under alternative valid weight sets and report rank range."""
    from .fit_score import score_employer
    rows = []
    for i, weights in enumerate(weight_sets):
        for profile in profiles:
            result = score_employer(profile, weights)
            rows.append({"weight_scenario": i + 1, "industry": profile.industry,
                         "score": result["fit_score"]})
    scores = pd.DataFrame(rows)
    scores["rank"] = scores.groupby("weight_scenario")["score"].rank(
        ascending=False, method="min")
    return (scores.groupby("industry")["rank"]
            .agg(best_rank="min", worst_rank="max", average_rank="mean")
            .reset_index())
