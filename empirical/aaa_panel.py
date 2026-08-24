import pandas as pd


REQUIRED_COLUMNS = (
    "entity",
    "agency",
    "rating",
    "start_year",
    "end_year",
    "evidence_id",
)


def validate_rating_intervals(intervals: pd.DataFrame) -> bool:
    missing = [c for c in REQUIRED_COLUMNS if c not in intervals.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if (intervals["start_year"] > intervals["end_year"]).any():
        raise ValueError("start_year cannot exceed end_year")

    return True


def build_aaa_membership_panel(
    intervals: pd.DataFrame,
    start_year: int,
    end_year: int,
    primary_agency: str = "S&P",
) -> pd.DataFrame:
    validate_rating_intervals(intervals)
    if start_year > end_year:
        raise ValueError("start_year must not exceed end_year")

    aaa = intervals[intervals["rating"] == "AAA"].copy()
    entities = sorted(intervals["entity"].unique())
    base = pd.MultiIndex.from_product(
        [entities, range(start_year, end_year + 1)],
        names=["entity", "year"],
    ).to_frame(index=False)

    primary = aaa[aaa["agency"] == primary_agency]
    primary_rows = []
    any_rows = []

    for _, row in aaa.iterrows():
        years = range(max(start_year, int(row["start_year"])), min(end_year, int(row["end_year"])) + 1)
        for year in years:
            any_rows.append((row["entity"], year))

    for _, row in primary.iterrows():
        years = range(max(start_year, int(row["start_year"])), min(end_year, int(row["end_year"])) + 1)
        for year in years:
            primary_rows.append((row["entity"], year))

    primary_set = set(primary_rows)
    any_set = set(any_rows)

    base["aaa_primary_member"] = base.apply(
        lambda r: int((r["entity"], r["year"]) in primary_set), axis=1
    )
    base["aaa_any_agency_member"] = base.apply(
        lambda r: int((r["entity"], r["year"]) in any_set), axis=1
    )

    return base
