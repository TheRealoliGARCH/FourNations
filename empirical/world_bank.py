import json
from pathlib import Path

import pandas as pd
import requests


def load_config(path="data/config/world_bank_series.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_indicator(countries, indicator, start_year, end_year, config_path="data/config/world_bank_series.json"):
    cfg = load_config(config_path)
    country_key = ";".join(countries)
    url = (
        f"{cfg['base_url']}/country/{country_key}/indicator/{indicator}"
        f"?format={cfg['format']}&source={cfg['source']}"
        f"&date={start_year}:{end_year}&per_page={cfg['per_page']}"
    )
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    payload = response.json()
    if len(payload) < 2 or payload[1] is None:
        return pd.DataFrame(columns=["country", "iso3c", "year", "value", "indicator"])

    rows = []
    for obs in payload[1]:
        rows.append(
            {
                "country": obs["country"]["value"],
                "iso3c": obs.get("countryiso3code"),
                "year": int(obs["date"]),
                "value": obs["value"],
                "indicator": indicator,
            }
        )
    return pd.DataFrame(rows)


def write_raw(df, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
