from pathlib import Path
import shutil

from empirical.generate_and_validate_structural_outputs import main


def test_generation_entrypoint_creates_all_outputs(tmp_path, monkeypatch):
    repo = Path(__file__).resolve().parents[1]
    for source in ("data", "empirical"):
        shutil.copytree(repo / source, tmp_path / source)
    monkeypatch.setattr(
        "empirical.generate_and_validate_structural_outputs.Path",
        lambda *args, **kwargs: Path(tmp_path / "empirical/generate_and_validate_structural_outputs.py"),
    )
    main()
    assert (tmp_path / "results/genuine_panel_documented_scenarios.csv").exists()
    assert (tmp_path / "results/fournations_cardinality_invariance.csv").exists()
    assert (tmp_path / "results/fournations_classification_changes.csv").exists()
    assert (tmp_path / "results/fournations_four_nation_years.csv").exists()
