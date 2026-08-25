import pandas as pd


def cardinality_regimes(diagnostic):
    rows = []
    for scenario, group in diagnostic.groupby("scenario", sort=True):
        counts = group["genuine_count"].value_counts().sort_index()
        total = len(group)
        for genuine_count, years in counts.items():
            rows.append({
                "scenario": scenario,
                "genuine_count": int(genuine_count),
                "year_count": int(years),
                "year_share": float(years / total),
            })
    return pd.DataFrame(rows)


def regime_transitions(diagnostic):
    rows = []
    for scenario, group in diagnostic.groupby("scenario", sort=True):
        group = group.sort_values("year").reset_index(drop=True)
        previous = group["genuine_count"].shift(1)
        changed = group.loc[previous.notna() & group["genuine_count"].ne(previous)]
        for _, row in changed.iterrows():
            prior_count = int(previous.loc[row.name])
            rows.append({
                "scenario": scenario,
                "year": int(row["year"]),
                "from_genuine_count": prior_count,
                "to_genuine_count": int(row["genuine_count"]),
                "delta_genuine_count": int(row["genuine_count"] - prior_count),
            })
    return pd.DataFrame(rows)


def baseline_deviations(diagnostic, baseline_name="baseline"):
    baseline = diagnostic.loc[diagnostic["scenario"] == baseline_name, ["year", "genuine_count"]].rename(
        columns={"genuine_count": "baseline_genuine_count"}
    )
    out = diagnostic.merge(baseline, on="year", how="left")
    out["genuine_count_delta_from_baseline"] = out["genuine_count"] - out["baseline_genuine_count"]
    out["four_nation_classification_delta_from_baseline"] = (
        out["is_four_nation_year"] != out.groupby("year")["is_four_nation_year"].transform("first")
    )
    return out[[
        "scenario", "year", "genuine_count", "baseline_genuine_count",
        "genuine_count_delta_from_baseline", "is_four_nation_year",
        "four_nation_classification_delta_from_baseline",
    ]]


def focal_window(diagnostic, start_year=1958, end_year=1965):
    return diagnostic.loc[
        diagnostic["year"].between(start_year, end_year),
        ["scenario", "year", "genuine_count", "distance_from_target", "is_four_nation_year"],
    ].sort_values(["scenario", "year"]).reset_index(drop=True)
