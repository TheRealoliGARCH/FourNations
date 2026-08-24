import pandas as pd

from empirical.genuine_nation_panel import (
    annual_genuine_nation_counts,
    merge_genuine_nation_panels,
)


def test_union_rule():
    nuclear = pd.DataFrame(
        {
            "entity": ["A", "B"],
            "year": [2020, 2020],
            "nuclear_member": [1, 0],
        }
    )
    aaa = pd.DataFrame(
        {
            "entity": ["A", "B", "C"],
            "year": [2020, 2020, 2020],
            "aaa_primary_member": [0, 1, 0],
            "aaa_any_agency_member": [0, 1, 1],
        }
    )
    out = merge_genuine_nation_panels(nuclear, aaa)
    assert out["genuine_primary"].sum() == 2
    assert out["genuine_extended"].sum() == 3


def test_annual_counts():
    panel = pd.DataFrame(
        {
            "year": [2020, 2020],
            "genuine_primary": [1, 1],
            "genuine_extended": [1, 1],
        }
    )
    counts = annual_genuine_nation_counts(panel)
    assert counts.iloc[0]["N_genuine_primary"] == 2
    assert counts.iloc[0]["N_genuine_extended"] == 2
