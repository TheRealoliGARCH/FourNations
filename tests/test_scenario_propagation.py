import pandas as pd

from empirical.propagate_nuclear_scenarios import apply_onset_scenario, merge_with_shield
from empirical.run_scenario_invariance import annual_counts, compare_to_baseline, affected_years


def test_later_onset_changes_only_intermediate_years():
    baseline = apply_onset_scenario(pd.DataFrame([{"entity": "India", "onset_year": 1974}]), "baseline", 1973, 1999)
    alternative = apply_onset_scenario(pd.DataFrame([{"entity": "India", "onset_year": 1998}]), "india_1998", 1973, 1999)
    shield = pd.DataFrame({"entity": ["India"] * 27, "year": list(range(1973, 2000)), "snp_shield_member": [pd.NA] * 27})
    base_g = merge_with_shield(baseline, shield)
    alt_g = merge_with_shield(alternative, shield)
    panel = pd.concat([base_g, alt_g], ignore_index=True)
    comparison = compare_to_baseline(annual_counts(panel))
    affected = affected_years(comparison)
    assert affected["year"].min() == 1974
    assert affected["year"].max() == 1997
    assert set(affected["genuine_count_delta"]) == {-1}


def test_unresolved_shield_remains_missing_without_nuclear_membership():
    nuclear = pd.DataFrame({"scenario": ["baseline"], "entity": ["X"], "year": [2000], "nuclear_member": [0]})
    shield = pd.DataFrame({"entity": ["X"], "year": [2000], "snp_shield_member": [pd.NA]})
    panel = merge_with_shield(nuclear, shield)
    assert pd.isna(panel.loc[0, "genuine_member"])
