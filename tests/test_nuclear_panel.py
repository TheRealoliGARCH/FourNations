import pandas as pd

from empirical.nuclear_panel import build_nuclear_membership_panel


def test_membership_switches_at_onset():
    onsets = pd.DataFrame(
        {
            "entity": ["A"],
            "onset_year": [1950],
            "onset_interpretation": ["test"],
            "evidence_id": ["x"],
        }
    )
    panel = build_nuclear_membership_panel(onsets, 1949, 1951)
    assert panel["nuclear_member"].tolist() == [0, 1, 1]


def test_invalid_range_rejected():
    onsets = pd.DataFrame(
        {
            "entity": ["A"],
            "onset_year": [1950],
            "onset_interpretation": ["test"],
            "evidence_id": ["x"],
        }
    )
    try:
        build_nuclear_membership_panel(onsets, 1951, 1950)
    except ValueError:
        return
    raise AssertionError("Expected ValueError")
