import pandas as pd

from empirical.four_nation_test import prepare_historical_panel, risk_difference


def test_prepares_threshold_indicator():
    df = pd.DataFrame(
        {
            "system_id": ["a", "a", "b"],
            "year": [1, 2, 3],
            "N_powers": [4, 5, 6],
            "crisis_5y": [0, 1, 1],
            "source_set": ["x", "x", "y"],
        }
    )
    result = prepare_historical_panel(df)
    assert result["N_gt_4"].tolist() == [0, 1, 1]


def test_risk_difference():
    df = pd.DataFrame(
        {
            "system_id": ["a", "a", "b", "b"],
            "year": [1, 2, 3, 4],
            "N_powers": [4, 3, 5, 6],
            "crisis_5y": [0, 0, 1, 1],
            "source_set": ["x", "x", "y", "y"],
        }
    )
    assert risk_difference(df) == 1.0
