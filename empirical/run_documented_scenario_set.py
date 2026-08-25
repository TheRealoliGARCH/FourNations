from pathlib import Path
import pandas as pd

from empirical.build_snp_shield_panel import build_snp_shield_panel
from empirical.propagate_nuclear_scenarios import apply_onset_scenario, merge_with_shield
from empirical.run_scenario_invariance import annual_counts, compare_to_baseline, affected_years


def build_scenario_onsets(scenarios_path="data/raw/nuclear_onset_scenarios.csv", seed_path="data/raw/nuclear_onsets_seed.csv"):
    scenarios = pd.read_csv(scenarios_path)
    seed = pd.read_csv(seed_path)
    sensitive = set(scenarios["entity"])
    fixed = seed.loc[~seed["entity"].isin(sensitive), ["entity", "onset_year"]]
    names = list(dict.fromkeys(scenarios["scenario"]))
    out = {}
    for name in names:
        variable = scenarios.loc[scenarios["scenario"] == name, ["entity", "onset_year"]]
        out[name] = pd.concat([fixed, variable], ignore_index=True)
    return out


def run_documented_scenarios(start_year=1945, end_year=2025, output_dir="results"):
    shield = build_snp_shield_panel(start_year=start_year, end_year=end_year)
    panels = []
    for scenario, onsets in build_scenario_onsets().items():
        nuclear = apply_onset_scenario(onsets, scenario, start_year, end_year)
        panels.append(merge_with_shield(nuclear, shield))
    genuine = pd.concat(panels, ignore_index=True)
    counts = annual_counts(genuine)
    comparison = compare_to_baseline(counts)
    affected = affected_years(comparison)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    genuine.to_csv(output / "genuine_panel_documented_scenarios.csv", index=False)
    comparison.to_csv(output / "genuine_scenario_comparison.csv", index=False)
    affected.to_csv(output / "genuine_scenario_affected_years.csv", index=False)
    return genuine, comparison, affected


if __name__ == "__main__":
    run_documented_scenarios()
