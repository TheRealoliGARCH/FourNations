import pandas as pd


def annual_genuine_count(panel):
    return (
        panel.groupby(["scenario", "year"], dropna=False)["genuine_member"]
        .apply(lambda x: int((x == 1).sum()))
        .rename("genuine_count")
        .reset_index()
    )


def four_nation_cardinality_diagnostic(panel, target=4):
    counts = annual_genuine_count(panel)
    counts["target"] = target
    counts["distance_from_target"] = counts["genuine_count"] - target
    counts["is_four_nation_year"] = counts["genuine_count"] == target
    return counts


def scenario_cardinality_invariance(panel, target=4, baseline_name="baseline"):
    diagnostic = four_nation_cardinality_diagnostic(panel, target=target)
    baseline = diagnostic.loc[
        diagnostic["scenario"] == baseline_name,
        ["year", "genuine_count", "distance_from_target", "is_four_nation_year"],
    ].rename(columns={
        "genuine_count": "baseline_genuine_count",
        "distance_from_target": "baseline_distance_from_target",
        "is_four_nation_year": "baseline_is_four_nation_year",
    })
    out = diagnostic.merge(baseline, on="year", how="left")
    out["count_delta_from_baseline"] = out["genuine_count"] - out["baseline_genuine_count"]
    out["four_nation_classification_changed"] = (
        out["is_four_nation_year"] != out["baseline_is_four_nation_year"]
    )
    return out
