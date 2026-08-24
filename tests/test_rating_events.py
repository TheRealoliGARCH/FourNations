import pandas as pd
from empirical.rating_events import events_to_annual_membership


def test_event_state_carries_forward_only_after_first_event():
    events = pd.DataFrame(
        {
            "entity": ["A", "A"],
            "agency": ["S&P", "S&P"],
            "event_date": ["2000-06-01", "2002-01-01"],
            "rating": ["AAA", "AA+"],
            "action": ["upgrade", "downgrade"],
            "evidence_id": ["e1", "e2"],
        }
    )
    out = events_to_annual_membership(events, 1999, 2002)
    assert out["aaa_member"].tolist() == [pd.NA, 1, 1, 0]


def test_unknown_history_is_missing_not_zero():
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
    out = events_to_annual_membership(events, 2000, 2001)
    assert pd.isna(out.iloc[0]["aaa_member"])
    assert out.iloc[1]["aaa_member"] == 1
