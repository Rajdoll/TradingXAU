from collections import namedtuple

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

from core.config import SWING_WINDOW

SwingPoints = namedtuple("SwingPoints", ["highs", "lows"])


def detect_swings(df: pd.DataFrame, window: int = SWING_WINDOW) -> SwingPoints:
    highs_arr = df["High"].to_numpy()
    lows_arr  = df["Low"].to_numpy()

    high_idx = argrelextrema(highs_arr, np.greater, order=window)[0]
    low_idx  = argrelextrema(lows_arr,  np.less,    order=window)[0]

    swing_highs = df["High"].iloc[high_idx] if len(high_idx) else pd.Series(dtype=float)
    swing_lows  = df["Low"].iloc[low_idx]   if len(low_idx)  else pd.Series(dtype=float)

    return SwingPoints(highs=swing_highs, lows=swing_lows)