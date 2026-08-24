import pandas as pd

from empirical.build_snp_shield_panel import build_snp_shield_panel


def build_shield_diagnostics(start_year=1950, end_year=2025):
    panel = build_snp_shield_panel(start_year=start_year, end_year=end_year)
    rows = []
    for year, group in panel.groupby("year"):
        observed = group["snp_shield_member"].notna()
        rows.append(
            {
                "year": year,
                "candidate_count": int(group["entity"].nunique()),
                "observed_count": int(observed.sum()),
                "missing_count": int((~observed).sum()),
                "aaa_count": int((group["snp_shield_member"] == 1).sum()),
                "non_aaa_count": int((group["snp_shield_member"] == 0).sum()),
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(build_shield_diagnostics().to_csv(index=False))
