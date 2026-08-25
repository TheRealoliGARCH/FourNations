import pandas as pd


def _intervals(years):
    years = sorted(set(int(year) for year in years))
    if not years:
        return ""
    intervals = []
    start = previous = years[0]
    for year in years[1:]:
        if year == previous + 1:
            previous = year
        else:
            intervals.append(f"{start}-{previous}" if start != previous else str(start))
            start = previous = year
    intervals.append(f"{start}-{previous}" if start != previous else str(start))
    return ";".join(intervals)


def sensitivity_summary(diagnostic, baseline_name="baseline"):
    baseline = diagnostic.loc[diagnostic["scenario"] == baseline_name].set_index("year")
    baseline_years = set(baseline.index[baseline["is_four_nation_year"]])
    rows = []
    for scenario, group in diagnostic.groupby("scenario", sort=True):
        current = group.set_index("year").reindex(baseline.index)
        delta = current["genuine_count"] - baseline["genuine_count"]
        deviation_years = delta.index[delta.ne(0)].tolist()
        current_years = set(current.index[current["is_four_nation_year"]])
        union = baseline_years | current_years
        intersection = baseline_years & current_years
        rows.append({
            "scenario": scenario,
            "deviation_year_count": int(len(deviation_years)),
            "deviation_intervals": _intervals(deviation_years),
            "maximum_absolute_cardinality_deviation": int(delta.abs().max()),
            "four_nation_baseline_year_count": len(baseline_years),
            "four_nation_scenario_year_count": len(current_years),
            "four_nation_overlap_year_count": len(intersection),
            "four_nation_union_year_count": len(union),
            "four_nation_jaccard_similarity": float(len(intersection) / len(union)) if union else 1.0,
            "four_nation_classification_change_count": int((current["is_four_nation_year"] != baseline["is_four_nation_year"]).sum()),
            "four_nation_classification_invariant": bool((current["is_four_nation_year"] == baseline["is_four_nation_year"]).all()),
        })
    return pd.DataFrame(rows)


def deviation_detail(diagnostic, baseline_name="baseline"):
    baseline = diagnostic.loc[diagnostic["scenario"] == baseline_name, ["year", "genuine_count"]].rename(columns={"genuine_count": "baseline_genuine_count"})
    out = diagnostic.merge(baseline, on="year", how="left")
    out["genuine_count_delta_from_baseline"] = out["genuine_count"] - out["baseline_genuine_count"]
    return out.loc[(out["scenario"] != baseline_name) & out["genuine_count_delta_from_baseline"].ne(0)].sort_values(["scenario", "year"]).reset_index(drop=True)
