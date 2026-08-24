import pandas as pd

from empirical.aaa_panel import build_aaa_membership_panel


def test_primary_and_any_agency_membership():
    intervals = pd.DataFrame(
        {
            "entity": ["A", "B"],
            "agency": ["S&P", "Fitch"],
            "rating": ["AAA", "AAA"],
            "start_year": [2000, 2000],
            "end_year": [2001, 2001],
            "evidence_id": ["x", "y"],
        }
    )
    out = build_aaa_membership_panel(intervals, 2000, 2001)
    a = out[out["entity"] == "A"]
    b = out[out["entity"] == "B"]
    assert a["aaa_primary_member"].tolist() == [1, 1]
    assert a["aaa_any_agency_member"].tolist() == [1, 1]
    assert b["aaa_primary_member"].tolist() == [0, 0]
    assert b["aaa_any_agency_member"].tolist() == [1, 1]
