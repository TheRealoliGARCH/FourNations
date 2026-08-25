from empirical.run_fournations_structural_outputs import run


def test_generated_panel_has_only_documented_scenarios(tmp_path):
    panel, diagnostic, changes = run(base_dir=".", output_dir=tmp_path)
    expected = {
        "baseline",
        "india_overt_1998",
        "israel_late_1966",
        "joint_documented",
    }
    assert set(panel["scenario"].dropna().unique()) == expected
    assert not panel["scenario"].isna().any()
    assert set(diagnostic["scenario"].unique()) == expected
    assert not diagnostic["scenario"].isna().any()
    assert not changes["scenario"].isna().any()


def test_scenario_summary_reports_invariant_window(tmp_path):
    run(base_dir=".", output_dir=tmp_path)
    import pandas as pd

    summary = pd.read_csv(tmp_path / "fournations_scenario_summary.csv")
    assert set(summary["scenario"]) == {
        "baseline",
        "india_overt_1998",
        "israel_late_1966",
        "joint_documented",
    }
    assert summary["four_nation_window_matches_baseline"].all()
    assert set(summary["four_nation_first_year"]) == {1960}
    assert set(summary["four_nation_last_year"]) == {1963}
    assert set(summary["four_nation_year_count"]) == {4}
