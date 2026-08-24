import pandas as pd

from empirical.build_shield_diagnostics import build_shield_diagnostics


def row(frame, year):
    return frame.loc[frame["year"] == year].iloc[0]


def test_early_panel_preserves_missingness():
    diagnostics = build_shield_diagnostics(1950, 1950)
    r = row(diagnostics, 1950)
    assert r["candidate_count"] == 11
    assert r["observed_count"] == 0
    assert r["missing_count"] == 11
    assert r["aaa_count"] == 0
    assert r["non_aaa_count"] == 0


def test_australia_observation_is_not_missing_after_1957():
    diagnostics = build_shield_diagnostics(1957, 1957)
    r = row(diagnostics, 1957)
    assert r["observed_count"] == 1
    assert r["non_aaa_count"] == 1


def test_counts_partition_candidate_universe():
    diagnostics = build_shield_diagnostics(2013, 2013)
    r = row(diagnostics, 2013)
    assert r["candidate_count"] == (
        r["missing_count"] + r["aaa_count"] + r["non_aaa_count"]
    )
