import pandas as pd

from empirical.rating_ingestion import (
    coverage_by_agency_year,
    normalize_rating_events,
)


def test_normalization_orders_events():
    events = pd.DataFrame(
        {
            "entity": ["A", "A"],
            "agency": ["S&P", "S&P"],
            "event_date": ["2001-01-01", "2000-01-01"],
            "rating": ["AA+", "AAA"],
            "action": ["downgrade", "snapshot"],
            "evidence_id": ["e2", "e1"],
        }
    )
    out = normalize_rating_events(events)
    assert out["event_date"].dt.year.tolist() == [2000, 2001]


def test_coverage_starts_with_first_observation():
    events = pd.DataFrame(
        {
            "entity": ["A"],
            "agency": ["S&P"],
            "event_date": ["2001-01-01"],
            "rating": ["AAA"],
            "action": ["snapshot"],
            "evidence_id": ["e1"],
        }
    )
    out = coverage_by_agency_year(events, 2000, 2002)
    assert out["rating_history_observed"].tolist() == [0, 1, 1]
