import pandas as pd

from empirical.build_snp_shield_panel import build_snp_shield_panel


def build_seed_nuclear_panel(
    onsets_path="data/raw/nuclear_onsets_seed.csv",
    start_year=1945,
    end_year=2025,
):
    onsets = pd.read_csv(onsets_path)
    years = pd.DataFrame({"year": range(start_year, end_year + 1)})
    entities = onsets[["entity", "onset_year"]].copy()
    entities["_key"] = 1
    years["_key"] = 1
    panel = entities.merge(years, on="_key").drop(columns="_key")
    panel["nuclear_member"] = (panel["year"] >= panel["onset_year"]).astype("Int64")
    return panel.drop(columns="onset_year").sort_values(["entity", "year"]).reset_index(drop=True)


def build_provisional_genuine_panel(start_year=1945, end_year=2025):
    shield = build_snp_shield_panel(start_year=start_year, end_year=end_year)
    nuclear = build_seed_nuclear_panel(start_year=start_year, end_year=end_year)

    entities = sorted(set(shield["entity"]) | set(nuclear["entity"]))
    years = pd.DataFrame({"year": range(start_year, end_year + 1)})
    universe = pd.DataFrame({"entity": entities})
    universe["_key"] = 1
    years["_key"] = 1
    panel = universe.merge(years, on="_key").drop(columns="_key")

    panel = panel.merge(shield[["entity", "year", "snp_shield_member"]], on=["entity", "year"], how="left")
    panel = panel.merge(nuclear, on=["entity", "year"], how="left")
    panel["nuclear_member"] = panel["nuclear_member"].fillna(0).astype("Int64")

    shield_observed = panel["snp_shield_member"].notna()
    panel["genuine_member"] = pd.Series(pd.NA, index=panel.index, dtype="Int64")
    panel.loc[panel["nuclear_member"] == 1, "genuine_member"] = 1
    panel.loc[(panel["nuclear_member"] == 0) & shield_observed, "genuine_member"] = panel.loc[(panel["nuclear_member"] == 0) & shield_observed, "snp_shield_member"].astype("Int64")

    panel["nuclear_source_status"] = "seed"
    panel["shield_source_status"] = panel["snp_shield_member"].map(lambda x: "observed" if pd.notna(x) else "missing")
    return panel.sort_values(["entity", "year"]).reset_index(drop=True)


if __name__ == "__main__":
    print(build_provisional_genuine_panel().to_csv(index=False))
