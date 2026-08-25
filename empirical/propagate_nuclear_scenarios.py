import pandas as pd


def apply_onset_scenario(onsets, scenario, start_year=1945, end_year=2025):
    rows = []
    for _, event in onsets.iterrows():
        entity = event["entity"]
        onset = int(event["onset_year"])
        for year in range(start_year, end_year + 1):
            rows.append({
                "scenario": scenario,
                "entity": entity,
                "year": year,
                "nuclear_member": int(year >= onset),
            })
    return pd.DataFrame(rows)


def scenario_delta(baseline, alternative):
    keys = ["entity", "year"]
    merged = baseline.merge(alternative, on=keys, suffixes=("_baseline", "_alternative"))
    merged["delta_nuclear_member"] = (
        merged["nuclear_member_alternative"] - merged["nuclear_member_baseline"]
    )
    return merged


def merge_with_shield(nuclear_panel, shield_panel):
    merged = nuclear_panel.merge(shield_panel, on=["entity", "year"], how="outer")
    merged["genuine_member"] = pd.Series(pd.NA, index=merged.index, dtype="Int64")
    merged.loc[merged["nuclear_member"] == 1, "genuine_member"] = 1
    observed_shield = merged["snp_shield_member"].notna() & merged["nuclear_member"].eq(0)
    merged.loc[observed_shield, "genuine_member"] = merged.loc[observed_shield, "snp_shield_member"].astype("Int64")
    return merged
