from empirical.fournations_robustness import deviation_detail, sensitivity_summary
from empirical.run_fournations_structural_outputs import run


def test_sensitivity_summary_confirms_full_four_nation_overlap(tmp_path):
    _, diagnostic, _ = run(base_dir=".", output_dir=tmp_path)
    summary = sensitivity_summary(diagnostic)
    assert set(summary["scenario"]) == {
        "baseline", "india_overt_1998", "israel_late_1966", "joint_documented"
    }
    assert (summary["four_nation_classification_invariant"]).all()
    assert (summary["four_nation_classification_change_count"] == 0).all()
    assert (summary["four_nation_jaccard_similarity"] == 1.0).all()
    assert (summary["four_nation_overlap_year_count"] == 4).all()


def test_deviation_detail_is_localized_and_excludes_four_nation_window(tmp_path):
    _, diagnostic, _ = run(base_dir=".", output_dir=tmp_path)
    detail = deviation_detail(diagnostic)
    assert not detail.empty
    assert not detail["year"].between(1960, 1963).any()
    assert (detail["genuine_count_delta_from_baseline"].abs() <= 1).all()


def test_sensitivity_artifacts_are_generated(tmp_path):
    run(base_dir=".", output_dir=tmp_path)
    assert (tmp_path / "fournations_sensitivity_summary.csv").exists()
    assert (tmp_path / "fournations_deviation_detail.csv").exists()
