import pandas as pd


REQUIRED_EVENT_COLUMNS = (
    "entity",
    "agency",
    "event_date",
    "rating",
    "action",
    "evidence_id",
)


def validate_rating_events(events: pd.DataFrame) -> bool:
    missing = [c for c in REQUIRED_EVENT_COLUMNS if c not in events.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    dates = pd.to_datetime(events["event_date"], errors="coerce")
    if dates.isna().any():
        raise ValueError("event_date contains invalid dates")

    if events.duplicated(["entity", "agency", "event_date"]).any():
        raise ValueError("Duplicate entity-agency-event_date records")

    return True


def events_to_annual_membership(
    events: pd.DataFrame,
    start_year: int,
    end_year: int,
    observation_month: int = 12,
    observation_day: int = 31,
) -> pd.DataFrame:
    validate_rating_events(events)
    if start_year > end_year:
        raise ValueError("start_year must not exceed end_year")

    work = events.copy()
    work["event_date"] = pd.to_datetime(work["event_date"])
    rows = []

    for (entity, agency), group in work.groupby(["entity", "agency"]):
        group = group.sort_values("event_date")
        for year in range(start_year, end_year + 1):
            obs_date = pd.Timestamp(year=year, month=observation_month, day=observation_day)
            prior = group[group["event_date"] <= obs_date]

            if prior.empty:
                rating = pd.NA
                evidence_id = pd.NA
            else:
                latest = prior.iloc[-1]
                rating = latest["rating"]
                evidence_id = latest["evidence_id"]

            rows.append(
                {
                    "entity": entity,
                    "agency": agency,
                    "year": year,
                    "rating": rating,
                    "aaa_member": pd.NA if pd.isna(rating) else int(rating == "AAA"),
                    "evidence_id": evidence_id,
                }
            )

    result = pd.DataFrame(rows)
    result["aaa_member"] = result["aaa_member"].astype("Int64")
    return result
