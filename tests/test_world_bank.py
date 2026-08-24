from empirical.world_bank import load_config


def test_world_bank_config_contains_core_indicators():
    cfg = load_config()
    assert cfg["provider"] == "World Bank"
    assert cfg["source"] == 2
    assert "GDP" in cfg["indicators"]
    assert "INFLATION" in cfg["indicators"]
    assert "CONSUMPTION_GROWTH" in cfg["indicators"]
