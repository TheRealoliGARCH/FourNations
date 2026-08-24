import json
from pathlib import Path
import pandas as pd

def load_config(path="data/config/sipri_sources.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_nuclear_membership(df: pd.DataFrame) -> bool:
    required = {"entity", "year", "nuclear_member", "evidence_id"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if (~df["nuclear_member"].isin([0, 1])).any():
        raise ValueError("nuclear_member must be binary")
    return True

def validate_milex(df: pd.DataFrame) -> bool:
    required = {"entity", "year", "evidence_id"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return True

def write_raw(df: pd.DataFrame, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
