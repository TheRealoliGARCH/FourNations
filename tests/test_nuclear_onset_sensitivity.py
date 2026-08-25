import pandas as pd

from empirical.nuclear_onset_sensitivity import build_scenario_nuclear_panel, scenario_differences


def test_scenario_engine_changes_only_years_between_alternative_onsets():
    onsets = pd.DataFrame({
        "scenario": ["baseline", "alternative"],
        "entity": ["X", "X"],
        "onset_year": [1970, 1972],
    })
    panel = build_scenario_nuclear_panel(onsets, 1969, 1973)
    diff = scenario_differences(panel)
    changed = diff.loc[(diff["scenario"] == "alternative") & diff["differs_from_baseline"], "year"].tolist()
    assert changed == [1970, 1971]


def test_baseline_has_no_difference_from_itself():
    onsets = pd.DataFrame({"scenario": ["baseline"], "entity": ["X"], "onset_year": [1970]})
    panel = build_scenario_nuclear_panel(onsets, 1969, 1971)
    diff = scenario_differences(panel)
    assert not diff["differs_from_baseline"].any()
