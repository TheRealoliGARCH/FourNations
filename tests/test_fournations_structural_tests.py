import pandas as pd

from empirical.fournations_structural_tests import (
    four_nation_cardinality_diagnostic,
    scenario_cardinality_invariance,
)


def panel(rows):
    return pd.DataFrame(rows)


def test_four_nation_year_is_detected_exactly():
    data = panel([
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "baseline", "year": 2001, "genuine_member": 1},
    ])
    out = four_nation_cardinality_diagnostic(data)
    assert bool(out.loc[out["year"] == 2000, "is_four_nation_year"].iloc[0])
    assert not bool(out.loc[out["year"] == 2001, "is_four_nation_year"].iloc[0])


def test_scenario_detects_changed_four_nation_classification():
    data = panel([
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "baseline", "year": 2000, "genuine_member": 1},
        {"scenario": "alternative", "year": 2000, "genuine_member": 1},
        {"scenario": "alternative", "year": 2000, "genuine_member": 1},
        {"scenario": "alternative", "year": 2000, "genuine_member": 1},
    ])
    out = scenario_cardinality_invariance(data)
    alt = out.loc[out["scenario"] == "alternative"].iloc[0]
    assert bool(alt["four_nation_classification_changed"])
