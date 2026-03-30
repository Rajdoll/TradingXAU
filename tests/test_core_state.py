import typing
import pytest


def test_pattern_result_importable():
    from core.state import PatternResult
    assert PatternResult is not None


def test_pattern_result_has_all_fields():
    from core.state import PatternResult
    hints = typing.get_type_hints(PatternResult)
    expected = {
        "name", "win_rate", "direction", "formation_pct",
        "entry_zone_low", "entry_zone_high", "invalidation_level",
        "tier", "skip",
    }
    assert hints.keys() == expected


def test_pattern_result_instantiates():
    from core.state import PatternResult
    pr: PatternResult = {
        "name": "Double Bottom",
        "win_rate": 0.93,
        "direction": "BUY",
        "formation_pct": 0.85,
        "entry_zone_low": 3280.0,
        "entry_zone_high": 3283.0,
        "invalidation_level": 3260.0,
        "tier": 1,
        "skip": False,
    }
    assert pr["name"] == "Double Bottom"
    assert pr["win_rate"] == 0.93
    assert pr["tier"] == 1
    assert pr["skip"] is False


def test_xau_state_importable():
    from core.state import XAUState
    assert XAUState is not None


def test_xau_state_has_all_fields():
    from core.state import XAUState
    hints = typing.get_type_hints(XAUState)
    expected = {
        # Data Layer (7)
        "ohlcv_h4", "ohlcv_m15", "fetch_timestamp", "current_price",
        "session", "news_risk", "news_events",
        # Pattern Layer (3)
        "patterns_found", "active_pattern", "no_pattern",
        # Confirmation Layer (6)
        "rsi_value", "rsi_signal", "candlestick_confirm", "candlestick_name",
        "sr_context", "tech_score",
        # Timeframe Layer (6)
        "h4_bias", "h4_last_hh", "h4_last_hl", "m15_aligned",
        "m15_entry_type", "tf_verdict",
        # Macro Layer (4)
        "dxy_trend", "tips_yield_direction", "macro_bias", "macro_confidence",
        # Debate Layer (5)
        "bull_arguments", "bear_arguments", "debate_score",
        "debate_verdict", "debate_key_reason",
        # Risk Layer (11)
        "account_balance", "risk_pct", "risk_usd", "lot_size", "sl_pips",
        "sl_price", "tp1_price", "tp2_price", "risk_reward",
        "risk_approved", "risk_reject_reason",
        # Output Layer (5)
        "confidence", "signal_id", "signal_summary",
        "journal_written", "pipeline_duration_s",
    }
    assert len(expected) == 47
    missing = expected - hints.keys()
    assert not missing, f"Missing XAUState fields: {missing}"


def test_xau_state_field_count():
    from core.state import XAUState
    hints = typing.get_type_hints(XAUState)
    assert len(hints) == 47
