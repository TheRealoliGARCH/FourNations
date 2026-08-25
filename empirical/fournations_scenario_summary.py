import pandas as pd


def build_scenario_summary(diagnostic, target=4):
    rows = []
    for scenario, group in diagnostic.groupby("scenario", sort=True, dropna=False):
        if pd.isna(scenario):
            raise ValueError("Scenario summary received unlabeled scenario rows")
        years = group.loc[group["is_four_nation_year"], "year"].tolist()
        rows.append({
            "scenario": scenario,
            "target": target,
            "four_nation_year_count": len(years),
            "four_nation_first_year": min(years) if years else pd.NA,
            "four_nation_last_year": max(years) if years else pd.NA,
            "four_nation_years": ";".join(str(year) for year in years),
            "min_genuine_count": int(group["genuine_count"].min()),
            "max_genuine_count": int(group["genuine_count"].max()),
        })
    return pd.DataFrame(rows)


def add_baseline_comparison(summary, baseline_name="baseline"):
    baseline = summary.loc[summary["scenario"] == baseline_name]
    if len(baseline) != 1:
        raise ValueError("Expected exactly one baseline scenario")
    baseline_row = baseline.iloc[0]
    out = summary.copy()
    out["four_nation_window_matches_baseline"] = (
        (out["four_nation_first_year"] == baseline_row["four_nation_first_year"])
        & (out["four_nation_last_year"] == baseline_row["four_nation_last_year"])
        & (out["four_nation_year_count"] == baseline_row["four_nation_year_count"])
    )
    return out
