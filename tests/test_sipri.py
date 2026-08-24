import pandas as pd
from empirical.sipri import load_config, validate_nuclear_membership

def test_sipri_config_has_required_datasets():
    cfg = load_config()
    assert cfg["provider"] == "SIPRI"
    assert cfg["nuclear"]["dataset"] == "World Nuclear Forces"
    assert cfg["military_expenditure"]["coverage_start"] == 1949

def test_validate_nuclear_membership():
    df = pd.DataFrame({"entity": ["A", "B"], "year": [2025, 2025], "nuclear_member": [1, 0], "evidence_id": ["x", "x"]})
    assert validate_nuclear_membership(df)
