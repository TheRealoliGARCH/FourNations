from empirical.run_documented_scenario_set import build_scenario_onsets, run_documented_scenarios


def test_each_scenario_contains_all_nine_nuclear_entities():
    scenarios = build_scenario_onsets()
    assert set(scenarios) == {"baseline", "israel_late_1966", "india_overt_1998", "joint_documented"}
    assert all(len(frame) == 9 for frame in scenarios.values())


def test_documented_scenario_intervals(tmp_path):
    _, _, affected = run_documented_scenarios(1945, 2025, tmp_path)
    israel = affected.loc[affected["scenario"] == "israel_late_1966"]
    india = affected.loc[affected["scenario"] == "india_overt_1998"]
    joint = affected.loc[affected["scenario"] == "joint_documented"]
    assert israel["year"].tolist() == [1966]
    assert india["year"].min() == 1974
    assert india["year"].max() == 1997
    assert set(india["genuine_count_delta"]) == {-1}
    assert joint["year"].min() == 1966
    assert joint["year"].max() == 1997
