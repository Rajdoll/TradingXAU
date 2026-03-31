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
