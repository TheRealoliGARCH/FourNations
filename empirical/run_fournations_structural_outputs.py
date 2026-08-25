from pathlib import Path
import sys
import argparse
import pandas as pd

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from empirical.build_snp_shield_panel import build_snp_shield_panel
from empirical.propagate_nuclear_scenarios import apply_onset_scenario, merge_with_shield
from empirical.fournations_structural_tests import four_nation_cardinality_diagnostic, scenario_cardinality_invariance
from empirical.fournations_scenario_summary import add_baseline_comparison, build_scenario_summary
from empirical.fournations_empirical_characterization import (
    baseline_deviations, cardinality_regimes, focal_window, regime_transitions,
)


def build_scenario_onsets(base_dir):
    seed = pd.read_csv(base_dir / "data/raw/nuclear_onsets_seed.csv")
    scenarios = pd.read_csv(base_dir / "data/raw/nuclear_onset_scenarios.csv")
    sensitive = {"Israel", "India", "Pakistan"}
    fixed = seed.loc[~seed["entity"].isin(sensitive), ["entity", "onset_year"]]
    out = {}
    for scenario, group in scenarios.groupby("scenario", sort=True):
        out[scenario] = pd.concat([fixed, group[["entity", "onset_year"]]], ignore_index=True)
    return out


def run(base_dir=".", output_dir="results", start_year=1950, end_year=2025):
    base_dir = Path(base_dir).resolve()
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = (base_dir / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    shield = build_snp_shield_panel(base_dir / "data/raw/sovereign_rating_events.csv", start_year, end_year)
    panels = []
    for scenario, onsets in build_scenario_onsets(base_dir).items():
        scenario_panel = merge_with_shield(apply_onset_scenario(onsets, scenario, start_year, end_year), shield)
        scenario_panel["scenario"] = scenario
        panels.append(scenario_panel)
    panel = pd.concat(panels, ignore_index=True).sort_values(["scenario", "entity", "year"])
    if panel["scenario"].isna().any():
        raise ValueError("Generated panel contains unlabeled scenario rows")
    diagnostic = four_nation_cardinality_diagnostic(panel)
    invariance = scenario_cardinality_invariance(panel)
    changes = invariance.loc[(invariance["scenario"] != "baseline") & invariance["four_nation_classification_changed"]].reset_index(drop=True)
    summary = add_baseline_comparison(build_scenario_summary(diagnostic))
    regimes = cardinality_regimes(diagnostic)
    transitions = regime_transitions(diagnostic)
    deviations = baseline_deviations(diagnostic)
    window = focal_window(diagnostic)
    outputs = {
        "genuine_panel_documented_scenarios.csv": panel,
        "fournations_cardinality_invariance.csv": diagnostic,
        "fournations_classification_changes.csv": changes,
        "fournations_scenario_summary.csv": summary,
        "fournations_cardinality_regimes.csv": regimes,
        "fournations_regime_transitions.csv": transitions,
        "fournations_baseline_deviations.csv": deviations,
        "fournations_focal_window.csv": window,
        "fournations_years.csv": diagnostic.loc[diagnostic["is_four_nation_year"], ["scenario", "year", "genuine_count", "distance_from_target"]].reset_index(drop=True),
    }
    for filename, frame in outputs.items():
        frame.to_csv(output_dir / filename, index=False)
    return panel, diagnostic, changes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--start-year", type=int, default=1950)
    parser.add_argument("--end-year", type=int, default=2025)
    args = parser.parse_args()
    run(args.base_dir, args.output_dir, args.start_year, args.end_year)
