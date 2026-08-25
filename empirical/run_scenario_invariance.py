import pandas as pd


def annual_counts(panel):
    rows = []
    for (scenario, year), group in panel.groupby(["scenario", "year"]):
        rows.append({
            "scenario": scenario,
            "year": year,
            "genuine_count": int((group["genuine_member"] == 1).sum()),
            "observed_non_member_count": int((group["genuine_member"] == 0).sum()),
            "unresolved_count": int(group["genuine_member"].isna().sum()),
        })
    return pd.DataFrame(rows)


def compare_to_baseline(counts, baseline_name="baseline"):
    base = counts.loc[counts["scenario"] == baseline_name, ["year", "genuine_count"]]
    base = base.rename(columns={"genuine_count": "baseline_genuine_count"})
    out = counts.merge(base, on="year", how="left")
    out["genuine_count_delta"] = out["genuine_count"] - out["baseline_genuine_count"]
    return out


def affected_years(comparison):
    return comparison.loc[
        (comparison["scenario"] != "baseline") & comparison["genuine_count_delta"].ne(0),
        ["scenario", "year", "genuine_count_delta"],
    ].reset_index(drop=True)
