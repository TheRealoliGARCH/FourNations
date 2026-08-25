import itertools
import pandas as pd


def build_onset_grid(base_onsets, candidate_years):
    entities = sorted(candidate_years)
    rows = []
    for values in itertools.product(*(candidate_years[entity] for entity in entities)):
        label_parts = []
        onset_map = dict(zip(entities, values))
        for entity in entities:
            label_parts.append(f"{entity.lower()}_{onset_map[entity]}")
        scenario = "grid__" + "__".join(label_parts)
        current = base_onsets.copy()
        for entity, year in onset_map.items():
            current.loc[current["entity"] == entity, "onset_year"] = year
        current["grid_scenario"] = scenario
        rows.append(current)
    return rows


def summarize_grid(grid_diagnostic, baseline_diagnostic):
    baseline = baseline_diagnostic.set_index("year")
    baseline_years = set(baseline.index[baseline["is_four_nation_year"]])
    rows = []
    for scenario, group in grid_diagnostic.groupby("scenario", sort=True):
        current = group.set_index("year").reindex(baseline.index)
        current_years = set(current.index[current["is_four_nation_year"]])
        changed = current["is_four_nation_year"] != baseline["is_four_nation_year"]
        rows.append({
            "scenario": scenario,
            "four_nation_year_count": len(current_years),
            "four_nation_overlap_year_count": len(current_years & baseline_years),
            "four_nation_classification_change_count": int(changed.sum()),
            "four_nation_classification_invariant": bool((~changed).all()),
        })
    return pd.DataFrame(rows)


def onset_grid_spec():
    return {
        "Israel": [1966, 1967],
        "India": [1974, 1998],
        "Pakistan": [1998, 1999],
    }
