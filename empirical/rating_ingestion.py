import pandas as pd

REQUIRED_COLUMNS = (
    "entity",
    "agency",
    "event_date",
    "rating",
    "action",
    "evidence_id",
)


def normalize_rating_events(events: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in events.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = events.copy()
    out["event_date"] = pd.to_datetime(out["event_date"], errors="raise")
    out["entity"] = out["entity"].astype(str).str.strip()
    out["agency"] = out["agency"].astype(str).str.strip()
    out["rating"] = out["rating"].astype(str).str.strip()
    out["action"] = out["action"].astype(str).str.strip()

    if out.duplicated(["entity", "agency", "event_date"]).any():
        raise ValueError("Duplicate entity-agency-event_date records")

    return out.sort_values(
        ["entity", "agency", "event_date"]
    ).reset_index(drop=True)


def coverage_by_agency_year(
    events: pd.DataFrame,
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    work = normalize_rating_events(events)
    rows = []

    for (entity, agency), group in work.groupby(["entity", "agency"]):
        first_year = int(group["event_date"].dt.year.min())
        for year in range(start_year, end_year + 1):
            rows.append(
                {
                    "entity": entity,
                    "agency": agency,
                    "year": year,
                    "rating_history_observed": int(year >= first_year),
                }
            )

    return pd.DataFrame(rows)
