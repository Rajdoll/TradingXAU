from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

from core.config import TICKER, H4_BARS, M15_BARS
from core.state import XAUState


def _detect_session() -> str:
    """Map current UTC hour to trading session name."""
    hour = datetime.now(timezone.utc).hour
    if 9 <= hour <= 13:
        return "LONDON"
    if 14 <= hour <= 23:
        return "NEW_YORK"
    return "ASIAN"


def _fetch_h4() -> pd.DataFrame:
    df = yf.download(TICKER, period="60d", interval="1h", progress=False)
    if df.empty:
        raise RuntimeError(f"yfinance returned empty H4 data for {TICKER}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df = df.resample("4h").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }).dropna()
    if df.empty:
        raise RuntimeError("H4 resample produced empty DataFrame")
    return df.tail(H4_BARS)


def _fetch_m15() -> pd.DataFrame:
    df = yf.download(TICKER, period="5d", interval="15m", progress=False)
    if df.empty:
        raise RuntimeError(f"yfinance returned empty M15 data for {TICKER}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    return df.dropna().tail(M15_BARS)


def fetch_data_node(state: XAUState) -> XAUState:
    # Implemented in Task 3
    raise NotImplementedError
