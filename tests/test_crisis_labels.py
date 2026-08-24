import pandas as pd

from empirical.crisis_labels import build_forward_crisis_labels


def test_labels_crisis_within_five_years():
    panel = pd.DataFrame(
        {"system_id": ["x", "x", "x"], "year": [1700, 1701, 1705]}
    )
    events = pd.DataFrame({"system_id": ["x"], "start_year": [1705]})
    out = build_forward_crisis_labels(panel, events, horizon=5)
    assert out["crisis_5y"].tolist() == [1, 1, 0]


def test_excludes_current_year_event():
    panel = pd.DataFrame({"system_id": ["x"], "year": [1705]})
    events = pd.DataFrame({"system_id": ["x"], "start_year": [1705]})
    out = build_forward_crisis_labels(panel, events, horizon=5)
    assert out["crisis_5y"].tolist() == [0]


def test_rejects_invalid_horizon():
    panel = pd.DataFrame({"system_id": ["x"], "year": [1700]})
    events = pd.DataFrame({"system_id": [], "start_year": []})
    try:
        build_forward_crisis_labels(panel, events, horizon=0)
    except ValueError:
        return
    raise AssertionError("Expected ValueError")
