import pandas as pd
from empirical.build_snp_shield_panel import build_snp_shield_panel

def value(panel, entity, year):
    return panel.loc[(panel["entity"] == entity) & (panel["year"] == year), "snp_shield_member"].iloc[0]

def test_remaining_candidate_histories():
    panel = build_snp_shield_panel(start_year=1974, end_year=1996)
    assert pd.isna(value(panel, "Norway", 1974))
    assert value(panel, "Norway", 1975) == 1
    assert pd.isna(value(panel, "Luxembourg", 1993))
    assert value(panel, "Luxembourg", 1994) == 1
    assert pd.isna(value(panel, "Liechtenstein", 1995))
    assert value(panel, "Liechtenstein", 1996) == 1

def test_netherlands_transition():
    panel = build_snp_shield_panel(start_year=2011, end_year=2015)
    assert value(panel, "Netherlands", 2012) == 1
    assert value(panel, "Netherlands", 2013) == 0
    assert value(panel, "Netherlands", 2015) == 1
