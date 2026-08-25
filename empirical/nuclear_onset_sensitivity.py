import pandas as pd


def build_scenario_nuclear_panel(onsets, start_year=1945, end_year=2025):
    required = {"scenario", "entity", "onset_year"}
    missing = required - set(onsets.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    years = pd.DataFrame({"year": range(start_year, end_year + 1)})
    parts = []
    for scenario, group in onsets.groupby("scenario", sort=True):
        entities = group[["entity", "onset_year"]].copy()
        entities["_key"] = 1
        y = years.copy()
        y["_key"] = 1
        panel = entities.merge(y, on="_key").drop(columns="_key")
        panel["scenario"] = scenario
        panel["nuclear_member"] = (panel["year"] >= panel["onset_year"]).astype("Int64")
        parts.append(panel.drop(columns="onset_year"))
    return pd.concat(parts, ignore_index=True).sort_values(["scenario", "entity", "year"]).reset_index(drop=True)


def scenario_differences(panel, baseline="baseline"):
    base = panel.loc[panel["scenario"] == baseline, ["entity", "year", "nuclear_member"]]
    base = base.rename(columns={"nuclear_member": "baseline_member"})
    merged = panel.merge(base, on=["entity", "year"], how="left")
    merged["differs_from_baseline"] = (
        merged["nuclear_member"].astype("Int64") != merged["baseline_member"].astype("Int64")
    ).fillna(False)
    return merged
