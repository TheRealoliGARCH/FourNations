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
from empirical.fournations_empirical_characterization import baseline_deviations, cardinality_regimes, focal_window, regime_transitions
from empirical.fournations_robustness import deviation_detail, sensitivity_summary
from empirical.fournations_onset_sensitivity import build_onset_grid, onset_grid_spec, summarize_grid


def build_scenario_onsets(base_dir):
    seed = pd.read_csv(base_dir / "data/raw/nuclear_onsets_seed.csv")
    scenarios = pd.read_csv(base_dir / "data/raw/nuclear_onset_scenarios.csv")
    sensitive = {"Israel", "India", "Pakistan"}
    fixed = seed.loc[~seed["entity"].isin(sensitive), ["entity", "onset_year"]]
    return {scenario: pd.concat([fixed, group[["entity", "onset_year"]]], ignore_index=True)
            for scenario, group in scenarios.groupby("scenario", sort=True)}


def _panel_for_onsets(onsets, scenario, shield, start_year, end_year):
    panel = merge_with_shield(apply_onset_scenario(onsets, scenario, start_year, end_year), shield)
    panel["scenario"] = scenario
    return panel


def run(base_dir=".", output_dir="results", start_year=1950, end_year=2025):
    base_dir = Path(base_dir).resolve()
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = (base_dir / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    shield = build_snp_shield_panel(base_dir / "data/raw/sovereign_rating_events.csv", start_year, end_year)
    scenario_onsets = build_scenario_onsets(base_dir)
    panels = [_panel_for_onsets(onsets, scenario, shield, start_year, end_year)
              for scenario, onsets in scenario_onsets.items()]
    panel = pd.concat(panels, ignore_index=True).sort_values(["scenario", "entity", "year"])
    if panel["scenario"].isna().any():
        raise ValueError("Generated panel contains unlabeled scenario rows")
    diagnostic = four_nation_cardinality_diagnostic(panel)
    baseline_diagnostic = diagnostic.loc[diagnostic["scenario"] == "baseline"].copy()
    grid_panels = []
    baseline_onsets = scenario_onsets["baseline"]
    for onsets in build_onset_grid(baseline_onsets, onset_grid_spec()):
        scenario = onsets["grid_scenario"].iloc[0]
        grid_panels.append(_panel_for_onsets(onsets.drop(columns=["grid_scenario"]), scenario, shield, start_year, end_year))
    grid_panel = pd.concat(grid_panels, ignore_index=True)
    grid_diagnostic = four_nation_cardinality_diagnostic(grid_panel)
    grid_summary = summarize_grid(grid_diagnostic, baseline_diagnostic)
    invariance = scenario_cardinality_invariance(panel)
    changes = invariance.loc[(invariance["scenario"] != "baseline") & invariance["four_nation_classification_changed"]].reset_index(drop=True)
    outputs = {
        "genuine_panel_documented_scenarios.csv": panel,
        "fournations_cardinality_invariance.csv": diagnostic,
        "fournations_classification_changes.csv": changes,
        "fournations_scenario_summary.csv": add_baseline_comparison(build_scenario_summary(diagnostic)),
        "fournations_cardinality_regimes.csv": cardinality_regimes(diagnostic),
        "fournations_regime_transitions.csv": regime_transitions(diagnostic),
        "fournations_baseline_deviations.csv": baseline_deviations(diagnostic),
        "fournations_focal_window.csv": focal_window(diagnostic),
        "fournations_sensitivity_summary.csv": sensitivity_summary(diagnostic),
        "fournations_deviation_detail.csv": deviation_detail(diagnostic),
        "fournations_onset_grid_summary.csv": grid_summary,
        "fournations_onset_grid_diagnostic.csv": grid_diagnostic,
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
