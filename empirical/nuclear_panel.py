import pandas as pd


REQUIRED_ONSET_COLUMNS = (
    "entity",
    "onset_year",
    "onset_interpretation",
    "evidence_id",
)


def validate_onsets(onsets: pd.DataFrame) -> bool:
    missing = [c for c in REQUIRED_ONSET_COLUMNS if c not in onsets.columns]
    if missing:
        raise ValueError(f"Missing required onset columns: {missing}")
    if onsets["onset_year"].isna().any():
        raise ValueError("onset_year cannot contain missing values")
    return True


def build_nuclear_membership_panel(onsets: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    validate_onsets(onsets)
    if start_year > end_year:
        raise ValueError("start_year must not exceed end_year")

    years = pd.DataFrame({"year": range(start_year, end_year + 1)})
    entities = onsets[["entity", "onset_year", "onset_interpretation", "evidence_id"]].copy()
    entities["_key"] = 1
    years["_key"] = 1
    panel = entities.merge(years, on="_key").drop(columns="_key")
    panel["nuclear_member"] = (panel["year"] >= panel["onset_year"]).astype(int)
    return panel.sort_values(["year", "entity"]).reset_index(drop=True)
