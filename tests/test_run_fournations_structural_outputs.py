from empirical.run_fournations_structural_outputs import build_outputs


def test_structural_outputs_cover_all_documented_scenarios(tmp_path):
    import shutil
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    shutil.copytree(root / "data", tmp_path / "data")
    panel, diagnostic, affected = build_outputs(base_dir=tmp_path, start_year=1945, end_year=2025)
    assert set(panel["scenario"].unique()) == {
        "baseline", "israel_late_1966", "india_overt_1998", "joint_documented"
    }
    assert set(diagnostic["scenario"].unique()) == set(panel["scenario"].unique())
    assert affected["scenario"].isin(panel["scenario"].unique()).all() if len(affected) else True
    assert (tmp_path / "results/fournations_cardinality_invariance.csv").exists()
