import pandas as pd


def test_documented_scenarios_are_explicitly_identified():
    scenarios = pd.read_csv("data/raw/nuclear_onset_scenarios.csv")
    documented = scenarios[scenarios["evidence_status"] == "documented"]
    assert set(documented["scenario"]) == {"israel_late_1966", "india_overt_1998", "joint_documented"}
    assert documented["evidence_id"].notna().all()


def test_israel_documented_alternative_is_1966():
    scenarios = pd.read_csv("data/raw/nuclear_onset_scenarios.csv")
    row = scenarios[(scenarios["scenario"] == "israel_late_1966") & (scenarios["entity"] == "Israel")].iloc[0]
    assert row["onset_year"] == 1966
    assert row["evidence_id"] == "SIPRI-YB-2001"


def test_india_overt_capability_alternative_is_1998():
    scenarios = pd.read_csv("data/raw/nuclear_onset_scenarios.csv")
    row = scenarios[(scenarios["scenario"] == "india_overt_1998") & (scenarios["entity"] == "India")].iloc[0]
    assert row["onset_year"] == 1998
    assert row["evidence_id"] == "SIPRI-YB-1999"


def test_no_unsupported_pakistan_alternative_is_introduced():
    scenarios = pd.read_csv("data/raw/nuclear_onset_scenarios.csv")
    pakistan = scenarios[scenarios["entity"] == "Pakistan"]
    assert set(pakistan["onset_year"]) == {1998}
