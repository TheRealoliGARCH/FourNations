import pandas as pd

from empirical.aaa_robustness import (
    build_agency_robustness_summary,
    build_extended_membership,
)


def test_extended_membership_preserves_missingness():
    annual = pd.DataFrame(
        {
            "entity": ["A", "A", "B"],
            "agency": ["S&P", "Fitch", "S&P"],
            "year": [2020, 2020, 2020],
            "aaa_member": [0, 1, pd.NA],
        }
    )
    out = build_extended_membership(annual).sort_values("entity")
    assert out.iloc[0]["aaa_any_agency_member"] == 1
    assert pd.isna(out.iloc[1]["aaa_any_agency_member"])


def test_agency_summary_counts_only_observed():
    annual = pd.DataFrame(
        {
            "entity": ["A", "B"],
            "agency": ["S&P", "S&P"],
            "year": [2020, 2020],
            "aaa_member": [1, pd.NA],
        }
    )
    out = build_agency_robustness_summary(annual)
    assert out.iloc[0]["observed_entities"] == 1
    assert out.iloc[0]["aaa_entities"] == 1
