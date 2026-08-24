import pandas as pd


def build_forward_crisis_labels(panel: pd.DataFrame, events: pd.DataFrame, horizon: int = 5) -> pd.DataFrame:
    required_panel = {"system_id", "year"}
    required_events = {"system_id", "start_year"}

    missing_panel = required_panel.difference(panel.columns)
    missing_events = required_events.difference(events.columns)

    if missing_panel:
        raise ValueError(f"Panel missing columns: {sorted(missing_panel)}")
    if missing_events:
        raise ValueError(f"Events missing columns: {sorted(missing_events)}")
    if horizon < 1:
        raise ValueError("horizon must be at least 1")

    out = panel.copy()
    out["crisis_5y"] = 0

    for idx, row in out.iterrows():
        future_events = events[
            (events["system_id"] == row["system_id"])
            & (events["start_year"] > row["year"])
            & (events["start_year"] <= row["year"] + horizon)
        ]
        out.loc[idx, "crisis_5y"] = int(not future_events.empty)

    return out
