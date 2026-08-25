from pathlib import Path
import pandas as pd

from empirical.run_fournations_structural_outputs import run


def main():
    root = Path(__file__).resolve().parents[1]
    panel, diagnostic, changes = run(root)
    if panel.empty:
        raise RuntimeError("Genuine scenario panel is empty")
    if diagnostic.empty:
        raise RuntimeError("FourNations cardinality diagnostic is empty")
    required = {"scenario", "year", "genuine_count", "distance_from_target", "is_four_nation_year"}
    missing = required.difference(diagnostic.columns)
    if missing:
        raise RuntimeError(f"Missing diagnostic columns: {sorted(missing)}")
    summary = (
        diagnostic.loc[diagnostic["is_four_nation_year"], ["scenario", "year", "genuine_count"]]
        .sort_values(["scenario", "year"])
        .reset_index(drop=True)
    )
    summary.to_csv(root / "results/fournations_four_nation_years.csv", index=False)
    for path in (
        root / "results/genuine_panel_documented_scenarios.csv",
        root / "results/fournations_cardinality_invariance.csv",
        root / "results/fournations_classification_changes.csv",
        root / "results/fournations_four_nation_years.csv",
    ):
        if not path.exists():
            raise RuntimeError(f"Expected output not generated: {path}")
    print(diagnostic.groupby("scenario")["is_four_nation_year"].sum().to_dict())
    print(f"classification_changes={len(changes)}")


if __name__ == "__main__":
    main()
