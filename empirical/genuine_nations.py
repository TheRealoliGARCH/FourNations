import pandas as pd


REQUIRED_MEMBERSHIP_COLUMNS = (
    "entity",
    "nuclear_member",
    "aaa_primary_member",
    "aaa_any_agency_member",
)


def classify_genuine_nations(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_MEMBERSHIP_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df.copy()
    out["genuine_primary"] = (
        (out["nuclear_member"].astype(bool))
        | (out["aaa_primary_member"].astype(bool))
    ).astype(int)
    out["genuine_extended"] = (
        (out["nuclear_member"].astype(bool))
        | (out["aaa_any_agency_member"].astype(bool))
    ).astype(int)
    return out
