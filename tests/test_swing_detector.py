import numpy as np
import pandas as pd
import pytest

from tools.swing_detector import detect_swings, SwingPoints


# ── Fixture helper ────────────────────────────────────────────────

def _make_swing_df(prices: list, freq: str = "4h") -> pd.DataFrame:
    """Build a minimal OHLCV DataFrame where High=prices, Low=prices-10."""
    index = pd.date_range("2026-01-01", periods=len(prices), freq=freq)
    return pd.DataFrame(
        {"High": prices, "Low": [p - 10 for p in prices]},
        index=index,
    )


# ── Core detection tests ──────────────────────────────────────────

# Series with two clear peaks and two clear valleys (window=1):
# prices: [3100, 3200, 3100, 3050, 3100, 3250, 3100, 3000, 3100]
# swing highs at idx 1 (3200) and idx 5 (3250)
# lows = prices-10: swing lows at idx 3 (3040) and idx 7 (2990)
_PRICES = [3100, 3200, 3100, 3050, 3100, 3250, 3100, 3000, 3100]


def test_detects_swing_highs():
    df = _make_swing_df(_PRICES)
    swings = detect_swings(df, window=1)
    assert list(swings.highs.values) == [3200.0, 3250.0]


def test_detects_swing_lows():
    df = _make_swing_df(_PRICES)
    swings = detect_swings(df, window=1)
    assert list(swings.lows.values) == [3040.0, 2990.0]


# ── Contract and behavioral tests ────────────────────────────────

def test_returns_series_indexed_by_datetime():
    df = _make_swing_df(_PRICES)
    swings = detect_swings(df, window=1)
    assert isinstance(swings.highs.index, pd.DatetimeIndex)
    assert isinstance(swings.lows.index, pd.DatetimeIndex)


def test_empty_highs_on_monotonic_increase():
    # Strictly increasing prices — no peak, so no swing highs
    prices = [3100.0, 3150.0, 3200.0, 3250.0, 3300.0]
    df = _make_swing_df(prices)
    swings = detect_swings(df, window=1)
    assert len(swings.highs) == 0
    assert isinstance(swings.highs, pd.Series)


def test_empty_lows_on_monotonic_decrease():
    # Strictly decreasing prices — lows also decrease monotonically → no valley
    prices = [3300.0, 3250.0, 3200.0, 3150.0, 3100.0]
    df = _make_swing_df(prices)
    swings = detect_swings(df, window=1)
    assert len(swings.lows) == 0
    assert isinstance(swings.lows, pd.Series)


def test_window_parameter_controls_sensitivity():
    # 15-bar series with multiple peaks — window=1 finds more highs than window=5
    prices = [3100, 3200, 3100, 3050, 3100, 3250, 3100, 3000,
              3100, 3200, 3100, 3050, 3100, 3250, 3100]
    df = _make_swing_df(prices)
    swings_w1 = detect_swings(df, window=1)
    swings_w5 = detect_swings(df, window=5)
    assert len(swings_w1.highs) > len(swings_w5.highs)


def test_last_high_and_low_via_iloc():
    # Mirrors the h4_last_hh / h4_last_hl consumer pattern in tf_arbiter
    df = _make_swing_df(_PRICES)
    swings = detect_swings(df, window=1)
    assert float(swings.highs.iloc[-1]) == 3250.0   # last swing high
    assert float(swings.lows.iloc[-1])  == 2990.0   # last swing low
