import pandas as pd

from empirical.aaa_panel import build_aaa_membership_panel
from empirical.nuclear_panel import build_nuclear_membership_panel
from empirical.genuine_nation_panel import (
    annual_genuine_nation_counts,
    merge_genuine_nation_panels,
)


def build_2026_genuine_panel(
    nuclear_onsets_path="data/raw/nuclear_onsets_seed.csv",
    aaa_intervals_path="data/raw/aaa_rating_intervals.csv",
):
    onsets = pd.read_csv(nuclear_onsets_path)
    ratings = pd.read_csv(aaa_intervals_path)

    nuclear = build_nuclear_membership_panel(onsets, 2026, 2026)
    aaa = build_aaa_membership_panel(ratings, 2026, 2026)

    panel = merge_genuine_nation_panels(
        nuclear[["entity", "year", "nuclear_member"]],
        aaa,
    )
    return panel, annual_genuine_nation_counts(panel)


if __name__ == "__main__":
    panel, counts = build_2026_genuine_panel()
    print(panel.to_csv(index=False))
    print(counts.to_csv(index=False))
