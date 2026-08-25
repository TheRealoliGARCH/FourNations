import pandas as pd

from empirical.build_provisional_genuine_panel import build_provisional_genuine_panel


def row(panel, entity, year):
    return panel.loc[(panel["entity"] == entity) & (panel["year"] == year)].iloc[0]


def test_nuclear_membership_overrides_missing_shield_history():
    panel = build_provisional_genuine_panel(1945, 1950)
    assert row(panel, "United States", 1945)["nuclear_member"] == 1
    assert row(panel, "United States", 1945)["genuine_member"] == 1


def test_missing_shield_remains_unresolved_without_nuclear_membership():
    panel = build_provisional_genuine_panel(1950, 1950)
    assert row(panel, "Australia", 1950)["nuclear_member"] == 0
    assert pd.isna(row(panel, "Australia", 1950)["snp_shield_member"])
    assert pd.isna(row(panel, "Australia", 1950)["genuine_member"])


def test_observed_non_aaa_and_non_nuclear_is_not_genuine():
    panel = build_provisional_genuine_panel(1957, 1957)
    assert row(panel, "Australia", 1957)["snp_shield_member"] == 0
    assert row(panel, "Australia", 1957)["nuclear_member"] == 0
    assert row(panel, "Australia", 1957)["genuine_member"] == 0


def test_seed_metadata_is_explicit():
    panel = build_provisional_genuine_panel(1998, 1998)
    assert set(panel["nuclear_source_status"]) == {"seed"}
