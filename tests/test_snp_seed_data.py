from empirical.build_snp_shield_panel import build_snp_shield_panel


def value(panel, entity, year):
    return panel.loc[
        (panel["entity"] == entity) & (panel["year"] == year),
        "snp_shield_member",
    ].iloc[0]


def test_seed_reconstructs_known_australia_transition():
    panel = build_snp_shield_panel(start_year=1974, end_year=2003)
    assert value(panel, "Australia", 1974) is None
    assert value(panel, "Australia", 1975) == 1
    assert value(panel, "Australia", 1986) == 0
    assert value(panel, "Australia", 2003) == 1


def test_seed_reconstructs_known_denmark_transition():
    panel = build_snp_shield_panel(start_year=1981, end_year=2001)
    assert value(panel, "Denmark", 1981) == 1
    assert value(panel, "Denmark", 1983) == 0
    assert value(panel, "Denmark", 2001) == 1


def test_missing_history_is_preserved():
    panel = build_snp_shield_panel(start_year=1950, end_year=1988)
    assert value(panel, "Switzerland", 1987) is None
    assert value(panel, "Switzerland", 1988) == 1
