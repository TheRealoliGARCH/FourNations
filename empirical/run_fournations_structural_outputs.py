from pathlib import Path
import pandas as pd

from empirical.build_snp_shield_panel import build_snp_shield_panel
from empirical.propagate_nuclear_scenarios import apply_onset_scenario, merge_with_shield
from empirical.fournations_structural_tests import four_nation_cardinality_diagnostic, scenario_cardinality_invariance


def build_scenario_onsets(base_dir):
    seed = pd.read_csv(base_dir / "data/raw/nuclear_onsets_seed.csv")
    scenarios = pd.read_csv(base_dir / "data/raw/nuclear_onset_scenarios.csv")
    sensitive = {"Israel", "India", "Pakistan"}
    fixed = seed.loc[~seed["entity"].isin(sensitive), ["entity", "onset_year"]]
    out = {}
    for scenario, group in scenarios.groupby("scenario", sort=True):
        current = group[["entity", "onset_year"]]
        out[scenario] = pd.concat([fixed, current], ignore_index=True)
    return out


def run(base_dir=".", output_dir="results", start_year=1950, end_year=2025):
    base_dir = Path(base_dir)
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = base_dir / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    shield = build_snp_shield_panel(
        events_path=base_dir / "data/raw/sovereign_rating_events.csv",
        start_year=start_year,
        end_year=end_year,
    )
    panels = []
    for scenario, onsets in build_scenario_onsets(base_dir).items():
        nuclear = apply_onset_scenario(onsets, scenario, start_year, end_year)
        panels.append(merge_with_shield(nuclear, shield))
    panel = pd.concat(panels, ignore_index=True).sort_values(["scenario", "entity", "year"])
    diagnostic = four_nation_cardinality_diagnostic(panel)
    invariance = scenario_cardinality_invariance(panel)
    changes = invariance.loc[
        (invariance["scenario"] != "baseline") & invariance["four_nation_classification_changed"]
    ].reset_index(drop=True)

    panel.to_csv(output_dir / "genuine_panel_documented_scenarios.csv", index=False)
    diagnostic.to_csv(output_dir / "fournations_cardinality_invariance.csv", index=False)
    changes.to_csv(output_dir / "fournations_classification_changes.csv", index=False)
    return panel, diagnostic, changes


if __name__ == "__main__":
    run()
