from unittest.mock import patch, MagicMock
from freezegun import freeze_time
import pandas as pd
import numpy as np
import pytest


# ── Helpers ──────────────────────────────────────────────────────

def _make_ohlcv_multiindex(n_rows=48):
    """OHLCV DataFrame with yfinance-style MultiIndex columns."""
    index = pd.date_range("2026-01-01", periods=n_rows, freq="1h")
    cols = ["Open", "High", "Low", "Close", "Volume"]
    data = {c: np.random.uniform(3200, 3300, n_rows) for c in cols}
    data["Volume"] = np.random.randint(1000, 5000, n_rows).astype(float)
    df = pd.DataFrame(data, index=index)
    df.columns = pd.MultiIndex.from_tuples([(c, "GC=F") for c in cols])
    return df


def _make_flat_ohlcv(n_rows=48, freq="1h"):
    """OHLCV DataFrame with flat columns (already processed)."""
    index = pd.date_range("2026-01-01", periods=n_rows, freq=freq)
    cols = ["Open", "High", "Low", "Close", "Volume"]
    data = {c: np.random.uniform(3200, 3300, n_rows) for c in cols}
    data["Volume"] = np.random.randint(1000, 5000, n_rows).astype(float)
    return pd.DataFrame(data, index=index)


# ── Session detection tests ───────────────────────────────────────

@freeze_time("2026-01-01 10:00:00")  # UTC 10:00
def test_session_london():
    from agents.data_fetcher import _detect_session
    assert _detect_session() == "LONDON"


@freeze_time("2026-01-01 15:00:00")  # UTC 15:00
def test_session_new_york():
    from agents.data_fetcher import _detect_session
    assert _detect_session() == "NEW_YORK"


@freeze_time("2026-01-01 03:00:00")  # UTC 03:00
def test_session_asian():
    from agents.data_fetcher import _detect_session
    assert _detect_session() == "ASIAN"


@freeze_time("2026-01-01 09:00:00")  # UTC 09:00 — London boundary
def test_session_boundary_london_start():
    from agents.data_fetcher import _detect_session
    assert _detect_session() == "LONDON"


@freeze_time("2026-01-01 14:00:00")  # UTC 14:00 — NY boundary
def test_session_boundary_ny_start():
    from agents.data_fetcher import _detect_session
    assert _detect_session() == "NEW_YORK"
