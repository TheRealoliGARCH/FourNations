import pandas as pd


def build_agency_robustness_summary(annual: pd.DataFrame) -> pd.DataFrame:
    required = {
        "entity",
        "agency",
        "year",
        "aaa_member",
    }
    missing = required.difference(annual.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    work = annual.copy()
    observed = work.dropna(subset=["aaa_member"])

    return (
        observed.groupby(["year", "agency"], as_index=False)
        .agg(
            observed_entities=("entity", "nunique"),
            aaa_entities=("aaa_member", "sum"),
        )
        .sort_values(["year", "agency"])
        .reset_index(drop=True)
    )


def build_extended_membership(annual: pd.DataFrame) -> pd.DataFrame:
    required = {"entity", "agency", "year", "aaa_member"}
    missing = required.difference(annual.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    rows = []
    for (entity, year), group in annual.groupby(["entity", "year"]):
        known = group["aaa_member"].dropna()
        if known.empty:
            value = pd.NA
        else:
            value = int((known == 1).any())
        rows.append(
            {
                "entity": entity,
                "year": year,
                "aaa_any_agency_member": value,
                "agencies_observed": int(known.shape[0]),
            }
        )

    return pd.DataFrame(rows)
