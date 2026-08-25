import pandas as pd

from empirical.build_provisional_genuine_panel import build_provisional_genuine_panel


def build_genuine_diagnostics(start_year=1945, end_year=2025):
    panel = build_provisional_genuine_panel(start_year=start_year, end_year=end_year)
    rows = []
    for year, group in panel.groupby("year"):
        rows.append(
            {
                "year": year,
                "universe_count": int(group["entity"].nunique()),
                "nuclear_count": int((group["nuclear_member"] == 1).sum()),
                "shield_count": int((group["snp_shield_member"] == 1).sum()),
                "genuine_count": int((group["genuine_member"] == 1).sum()),
                "unresolved_count": int(group["genuine_member"].isna().sum()),
            }
        )
    return pd.DataFrame(rows)
