import pandas as pd
from empirical.fournations_empirical_characterization import baseline_deviations, cardinality_regimes, focal_window, regime_transitions
from empirical.run_fournations_structural_outputs import run


def test_empirical_characterization_artifacts(tmp_path):
    _, diagnostic, _ = run(base_dir=".", output_dir=tmp_path)
    expected = {"baseline", "india_overt_1998", "israel_late_1966", "joint_documented"}
    for filename in [
        "fournations_cardinality_regimes.csv",
        "fournations_regime_transitions.csv",
        "fournations_baseline_deviations.csv",
        "fournations_focal_window.csv",
    ]:
        assert (tmp_path / filename).exists()
    assert set(cardinality_regimes(diagnostic)["scenario"]) == expected
    assert set(regime_transitions(diagnostic)["scenario"]) == expected


def test_focal_window_contains_invariant_four_nation_period(tmp_path):
    _, diagnostic, _ = run(base_dir=".", output_dir=tmp_path)
    window = focal_window(diagnostic)
    four = window.loc[window["is_four_nation_year"]]
    assert set(four["year"]) == {1960, 1961, 1962, 1963}
    assert set(four["scenario"]) == {"baseline", "india_overt_1998", "israel_late_1966", "joint_documented"}


def test_documented_scenario_deviations_do_not_change_four_nation_classification(tmp_path):
    _, diagnostic, _ = run(base_dir=".", output_dir=tmp_path)
    deviations = baseline_deviations(diagnostic)
    alternatives = deviations.loc[deviations["scenario"] != "baseline"]
    assert not alternatives["four_nation_classification_delta_from_baseline"].any()
    assert (alternatives.loc[alternatives["year"].between(1960, 1963), "genuine_count_delta_from_baseline"] == 0).all()
