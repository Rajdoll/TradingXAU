import pytest

import pandas as pd
from tools.swing_detector import detect_swings, SwingPoints
import patterns.double_bottom   # triggers PATTERN_REGISTRY.append
from patterns.base import PATTERN_REGISTRY
from patterns.double_bottom import detect_double_bottom


# ── Registry structural test ──────────────────────────────────────

def test_pattern_registry_is_list():
    from patterns.base import PATTERN_REGISTRY
    assert isinstance(PATTERN_REGISTRY, list)


# ── Fixture helpers ───────────────────────────────────────────────

def _make_double_bottom_df() -> pd.DataFrame:
    """5-bar W-shape with realistic OHLCV (High != Low), window=1.

    High: [3250, 3150, 3250, 3150, 3250]
    Low:  [3150, 3100, 3150, 3100, 3150]
    argrelextrema(High, np.greater, order=1): idx 2 → 3250.0 (neckline)
    argrelextrema(Low, np.less,    order=1): idx 1 → 3100.0, idx 3 → 3100.0
    neckline=3250.0, entry_zone_low=3250.0, entry_zone_high=3250.0*1.003=3257.75
    invalidation=3100.0 - 20*0.01 = 3099.8
    """
    index = pd.date_range("2026-01-01", periods=5, freq="4h")
    return pd.DataFrame({
        "High": [3250.0, 3150.0, 3250.0, 3150.0, 3250.0],
        "Low":  [3150.0, 3100.0, 3150.0, 3100.0, 3150.0],
    }, index=index)


def _db_swings() -> SwingPoints:
    return detect_swings(_make_double_bottom_df(), window=1)


# ── Detection tests ───────────────────────────────────────────────

def test_double_bottom_detects_valid_pattern():
    result = detect_double_bottom(_make_double_bottom_df(), _db_swings(), current_price=3200.0)
    assert result is not None
    assert result["name"] == "Double Bottom"


def test_double_bottom_direction_is_buy():
    result = detect_double_bottom(_make_double_bottom_df(), _db_swings(), current_price=3200.0)
    assert result["direction"] == "BUY"


def test_double_bottom_entry_zone_at_neckline():
    result = detect_double_bottom(_make_double_bottom_df(), _db_swings(), current_price=3250.0)
    # neckline = 3250.0 (swing high between the two lows)
    assert result["entry_zone_low"] == 3250.0
    assert result["entry_zone_high"] == pytest.approx(3250.0 * 1.003)


def test_double_bottom_formation_pct_capped_at_1():
    # current_price=3300 > neckline=3200 → formation_pct must be 1.0, not 1.03+
    result = detect_double_bottom(_make_double_bottom_df(), _db_swings(), current_price=3300.0)
    assert result["formation_pct"] == 1.0


def test_double_bottom_invalidation_below_lower_low():
    result = detect_double_bottom(_make_double_bottom_df(), _db_swings(), current_price=3200.0)
    # lower of the two lows = 3100.0; invalidation must be strictly below it
    assert result["invalidation_level"] < 3100.0


def test_double_bottom_returns_none_if_lows_too_far_apart():
    # low1=3100, low2=3163 → 63/3100 ≈ 2.03% > 1.5% tolerance → None
    idx = pd.date_range("2026-01-01", periods=5, freq="4h")
    df = pd.DataFrame({"High": [3200.0] * 5, "Low": [3100.0] * 5}, index=idx)
    swings = SwingPoints(
        highs=pd.Series([3200.0], index=[idx[2]]),
        lows=pd.Series([3100.0, 3163.0], index=[idx[1], idx[3]]),
    )
    assert detect_double_bottom(df, swings, current_price=3163.0) is None


def test_double_bottom_returns_none_if_fewer_than_2_lows():
    idx = pd.date_range("2026-01-01", periods=5, freq="4h")
    df = pd.DataFrame({"High": [3200.0] * 5, "Low": [3100.0] * 5}, index=idx)
    swings = SwingPoints(
        highs=pd.Series([3200.0], index=[idx[2]]),
        lows=pd.Series([3100.0], index=[idx[1]]),   # only 1 low
    )
    assert detect_double_bottom(df, swings, current_price=3150.0) is None


def test_double_bottom_returns_none_if_no_high_between_lows():
    # Two valid lows but no swing high exists between them → not a Double Bottom
    idx = pd.date_range("2026-01-01", periods=5, freq="4h")
    df = pd.DataFrame({"High": [3200.0] * 5, "Low": [3100.0] * 5}, index=idx)
    swings = SwingPoints(
        highs=pd.Series(dtype=float, index=pd.DatetimeIndex([])),  # no highs at all
        lows=pd.Series([3100.0, 3100.0], index=[idx[1], idx[3]]),
    )
    assert detect_double_bottom(df, swings, current_price=3150.0) is None


def test_pattern_registry_contains_detect_double_bottom():
    # patterns.double_bottom was imported at top of file — registry must contain it
    assert detect_double_bottom in PATTERN_REGISTRY
