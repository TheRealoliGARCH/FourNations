import pandas as pd

from empirical.rating_events import events_to_annual_membership


def test_year_end_uses_latest_event_on_or_before_december_31():
    events = pd.DataFrame(
        {
            "entity": ["A", "A"],
            "agency": ["S&P", "S&P"],
            "event_date": ["2025-01-10", "2025-11-30"],
            "rating": ["AAA", "AA+"],
            "action": ["affirmation", "downgrade"],
            "evidence_id": ["e1", "e2"],
        }
    )
    out = events_to_annual_membership(events, 2025, 2025)
    assert out.iloc[0]["rating"] == "AA+"
    assert out.iloc[0]["aaa_member"] == 0


def test_future_event_does_not_contaminate_prior_year():
    events = pd.DataFrame(
        {
            "entity": ["A", "A"],
            "agency": ["S&P", "S&P"],
            "event_date": ["2025-12-31", "2026-07-31"],
            "rating": ["AAA", "AA+"],
            "action": ["snapshot", "downgrade"],
            "evidence_id": ["e1", "e2"],
        }
    )
    out = events_to_annual_membership(events, 2025, 2025)
    assert out.iloc[0]["rating"] == "AAA"
    assert out.iloc[0]["aaa_member"] == 1
