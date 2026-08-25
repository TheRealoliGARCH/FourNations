from empirical.fournations_onset_sensitivity import build_onset_grid, onset_grid_spec, summarize_grid
from empirical.run_fournations_structural_outputs import build_scenario_onsets, run


def test_onset_grid_has_full_factorial_coverage():
    spec = onset_grid_spec()
    assert len(build_onset_grid(build_scenario_onsets(".")["baseline"], spec)) == 8


def test_grid_summary_is_generated_and_invariant(tmp_path):
    run(base_dir=".", output_dir=tmp_path)
    import pandas as pd
    summary = pd.read_csv(tmp_path / "fournations_onset_grid_summary.csv")
    assert len(summary) == 8
    assert summary["four_nation_classification_invariant"].all()
    assert (summary["four_nation_classification_change_count"] == 0).all()
    assert (summary["four_nation_overlap_year_count"] == 4).all()


def test_grid_diagnostic_artifact_exists(tmp_path):
    run(base_dir=".", output_dir=tmp_path)
    assert (tmp_path / "fournations_onset_grid_diagnostic.csv").exists()
