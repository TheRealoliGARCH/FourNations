import numpy as np
import pandas as pd

from empirical.schema import validate_historical_columns


def prepare_historical_panel(df):
    validate_historical_columns(df.columns)
    out = df.copy()
    out["N_gt_4"] = (out["N_powers"] > 4).astype(int)
    return out


def crisis_rate_by_threshold(df):
    panel = prepare_historical_panel(df)
    rates = panel.groupby("N_gt_4", dropna=False)["crisis_5y"].mean()
    return {
        "rate_N_le_4": float(rates.get(0, np.nan)),
        "rate_N_gt_4": float(rates.get(1, np.nan)),
    }


def risk_difference(df):
    rates = crisis_rate_by_threshold(df)
    return rates["rate_N_gt_4"] - rates["rate_N_le_4"]
