import pandas as pd

from empirical.rating_events import events_to_annual_membership


def build_snp_shield_panel(
    events_path="data/raw/sovereign_rating_events.csv",
    start_year=1950,
    end_year=2025,
):
    events = pd.read_csv(events_path)
    annual = events_to_annual_membership(events, start_year, end_year)
    annual = annual[annual["agency"] == "S&P"].copy()
    annual["snp_shield_member"] = annual["aaa_member"]
    return annual.sort_values(["entity", "year"]).reset_index(drop=True)


if __name__ == "__main__":
    print(build_snp_shield_panel().to_csv(index=False))
