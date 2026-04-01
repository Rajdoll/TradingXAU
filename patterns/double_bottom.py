# patterns/double_bottom.py — Double Bottom pattern detector (93% historical win rate, Tier 1)
from typing import Optional

import pandas as pd

from core.config import PIP_VALUE, SL_BUFFER_PIPS
from core.state import PatternResult
from patterns.base import PATTERN_REGISTRY
from tools.swing_detector import SwingPoints

WIN_RATE  = 0.93
TIER      = 1
TOLERANCE = 0.015   # max relative difference between the two lows


def detect_double_bottom(
    df: pd.DataFrame,
    swings: SwingPoints,
    current_price: float,
) -> Optional[PatternResult]:
    """Detect a Double Bottom (W-shape) pattern in H4 swing data.

    Returns PatternResult if two swing lows within 1.5% tolerance exist with a
    swing high (neckline) strictly between them. Returns None otherwise.
    """
    if len(swings.lows) < 2:
        return None

    low1 = float(swings.lows.iloc[-2])
    low2 = float(swings.lows.iloc[-1])

    if abs(low1 - low2) / min(low1, low2) > TOLERANCE:
        return None

    t1 = swings.lows.index[-2]
    t2 = swings.lows.index[-1]
    highs_between = swings.highs[
        (swings.highs.index > t1) & (swings.highs.index < t2)
    ]
    if highs_between.empty:
        return None

    neckline = float(highs_between.max())

    return PatternResult(
        name               = "Double Bottom",
        win_rate           = WIN_RATE,
        direction          = "BUY",
        formation_pct      = min(current_price / neckline, 1.0),
        entry_zone_low     = neckline,
        entry_zone_high    = neckline * 1.003,
        invalidation_level = min(low1, low2) - SL_BUFFER_PIPS * PIP_VALUE,
        tier               = TIER,
        skip               = False,
    )


PATTERN_REGISTRY.append(detect_double_bottom)
