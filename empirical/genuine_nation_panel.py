import pandas as pd


def merge_genuine_nation_panels(
    nuclear_panel: pd.DataFrame,
    aaa_panel: pd.DataFrame,
) -> pd.DataFrame:
    required_nuclear = {"entity", "year", "nuclear_member"}
    required_aaa = {
        "entity",
        "year",
        "aaa_primary_member",
        "aaa_any_agency_member",
    }

    missing_nuclear = required_nuclear.difference(nuclear_panel.columns)
    missing_aaa = required_aaa.difference(aaa_panel.columns)

    if missing_nuclear:
        raise ValueError(f"Nuclear panel missing: {sorted(missing_nuclear)}")
    if missing_aaa:
        raise ValueError(f"AAA panel missing: {sorted(missing_aaa)}")

    merged = nuclear_panel.merge(
        aaa_panel,
        on=["entity", "year"],
        how="outer",
    )

    for col in [
        "nuclear_member",
        "aaa_primary_member",
        "aaa_any_agency_member",
    ]:
        merged[col] = merged[col].fillna(0).astype(int)

    merged["genuine_primary"] = (
        (merged["nuclear_member"] == 1)
        | (merged["aaa_primary_member"] == 1)
    ).astype(int)

    merged["genuine_extended"] = (
        (merged["nuclear_member"] == 1)
        | (merged["aaa_any_agency_member"] == 1)
    ).astype(int)

    return merged.sort_values(["year", "entity"]).reset_index(drop=True)


def annual_genuine_nation_counts(panel: pd.DataFrame) -> pd.DataFrame:
    required = {"year", "genuine_primary", "genuine_extended"}
    missing = required.difference(panel.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    return (
        panel.groupby("year", as_index=False)
        .agg(
            N_genuine_primary=("genuine_primary", "sum"),
            N_genuine_extended=("genuine_extended", "sum"),
        )
    )
