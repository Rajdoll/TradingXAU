import pytest


def test_config_importable():
    import core.config
    assert core.config is not None


def test_invariant_risk_constants():
    from core.config import (
        LOT_SIZE, PIP_VALUE, MAX_SL_PIPS, MIN_SL_PIPS,
        SL_BUFFER_PIPS, MIN_RR, MAX_DAILY_LOSSES, NEWS_BUFFER_HOURS,
    )
    assert LOT_SIZE == 0.01
    assert PIP_VALUE == 0.01
    assert MAX_SL_PIPS == 100
    assert MIN_SL_PIPS == 15
    assert SL_BUFFER_PIPS == 20
    assert MIN_RR == 2.0
    assert MAX_DAILY_LOSSES == 2
    assert NEWS_BUFFER_HOURS == 2


def test_risk_usd_derived_from_balance_and_pct():
    from core.config import ACCOUNT_BALANCE, RISK_PCT, RISK_USD
    assert RISK_USD == ACCOUNT_BALANCE * RISK_PCT


def test_default_account_balance():
    from core.config import ACCOUNT_BALANCE
    assert ACCOUNT_BALANCE == 50.00


def test_default_risk_pct():
    from core.config import RISK_PCT
    assert RISK_PCT == 0.02


def test_data_config_constants():
    from core.config import TICKER, H4_BARS, M15_BARS, SWING_WINDOW
    assert TICKER == "GC=F"
    assert H4_BARS == 200
    assert M15_BARS == 200
    assert SWING_WINDOW == 5


def test_model_constants_are_strings():
    from core.config import ANALYST_MODEL, LIGHT_MODEL
    assert isinstance(ANALYST_MODEL, str)
    assert len(ANALYST_MODEL) > 0
    assert isinstance(LIGHT_MODEL, str)
    assert len(LIGHT_MODEL) > 0


def test_default_model_names():
    from core.config import ANALYST_MODEL, LIGHT_MODEL
    assert ANALYST_MODEL == "claude-sonnet-4-6"
    assert LIGHT_MODEL == "claude-haiku-4-5-20251001"


def test_api_key_constants_exist():
    from core.config import ANTHROPIC_API_KEY, FRED_API_KEY
    assert isinstance(ANTHROPIC_API_KEY, str)
    assert isinstance(FRED_API_KEY, str)
