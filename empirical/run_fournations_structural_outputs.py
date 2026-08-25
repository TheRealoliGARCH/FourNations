from pathlib import Path

import pandas as pd

from empirical.build_snp_shield_panel import build_snp_shield_panel
from empirical.fournations_structural_tests import scenario_cardinality_invariance
from empirical.propagate_nuclear_scenarios import apply_onset_scenario, merge_with_shield


def load_scenarios(scenario_path, seed_path):
    scenarios = pd.read_csv(scenario_path)
    seed = pd.read_csv(seed_path)
    unaffected = seed.loc[~seed["entity"].isin(["Israel", "India", "Pakistan"])]
    return [
        (scenario, pd.concat([group[["entity", "onset_year"]], unaffected[["entity", "onset_year"]]], ignore_index=True))
        for scenario, group in scenarios.groupby("scenario")
    ]


def build_outputs(base_dir=".", output_dir="results", start_year=1945, end_year=2025):
    base = Path(base_dir)
    scenario_path = base / "data/raw/nuclear_onset_scenarios.csv"
    seed_path = base / "data/raw/nuclear_onsets_seed.csv"
    events_path = base / "data/raw/sovereign_rating_events.csv"
    shield = build_snp_shield_panel(str(events_path), start_year=start_year, end_year=end_year)
    panels = []
    for scenario, onsets in load_scenarios(scenario_path, seed_path):
        nuclear = apply_onset_scenario(onsets, scenario, start_year, end_year)
        panels.append(merge_with_shield(nuclear, shield))
    panel = pd.concat(panels, ignore_index=True)
    diagnostic = scenario_cardinality_invariance(panel)
    affected = diagnostic.loc[diagnostic["four_nation_classification_changed"], ["scenario", "year", "genuine_count", "baseline_genuine_count", "count_delta_from_baseline"]]
    output = base / output_dir
    output.mkdir(parents=True, exist_ok=True)
    panel.to_csv(output / "genuine_panel_documented_scenarios.csv", index=False)
    diagnostic.to_csv(output / "fournations_cardinality_invariance.csv", index=False)
    affected.to_csv(output / "fournations_classification_changes.csv", index=False)
    return panel, diagnostic, affected


if __name__ == "__main__":
    build_outputs()
