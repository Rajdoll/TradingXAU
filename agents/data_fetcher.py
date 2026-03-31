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
    # Implemented in Task 2
    raise NotImplementedError


def _fetch_m15() -> pd.DataFrame:
    # Implemented in Task 2
    raise NotImplementedError


def fetch_data_node(state: XAUState) -> XAUState:
    # Implemented in Task 3
    raise NotImplementedError
