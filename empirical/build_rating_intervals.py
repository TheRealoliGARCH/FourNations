import pandas as pd

from empirical.rating_events import events_to_annual_membership


def annual_membership_to_intervals(annual: pd.DataFrame) -> pd.DataFrame:
    required = {"entity", "agency", "year", "rating", "aaa_member", "evidence_id"}
    missing = required.difference(annual.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    rows = []
    known = annual.dropna(subset=["aaa_member"]).copy()

    for (entity, agency, rating), group in known.groupby(["entity", "agency", "rating"], dropna=False):
        group = group.sort_values("year")
        run_start = None
        previous = None
        evidence = None

        for _, row in group.iterrows():
            year = int(row["year"])
            if run_start is None:
                run_start = year
                previous = year
                evidence = row["evidence_id"]
            elif year == previous + 1:
                previous = year
            else:
                rows.append(
                    {
                        "entity": entity,
                        "agency": agency,
                        "rating": rating,
                        "start_year": run_start,
                        "end_year": previous,
                        "evidence_id": evidence,
                    }
                )
                run_start = year
                previous = year
                evidence = row["evidence_id"]

        if run_start is not None:
            rows.append(
                {
                    "entity": entity,
                    "agency": agency,
                    "rating": rating,
                    "start_year": run_start,
                    "end_year": previous,
                    "evidence_id": evidence,
                }
            )

    return pd.DataFrame(rows)
