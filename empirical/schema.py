REQUIRED_HISTORICAL_COLUMNS = (
    "system_id",
    "year",
    "N_powers",
    "crisis_5y",
    "source_set",
)


def validate_historical_columns(columns):
    missing = [c for c in REQUIRED_HISTORICAL_COLUMNS if c not in columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True
