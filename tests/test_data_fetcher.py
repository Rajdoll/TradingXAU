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


# ── H4 fetch tests ───────────────────────────────────────────────

@patch("agents.data_fetcher.yf.download")
def test_fetch_h4_flattens_multiindex(mock_dl):
    from agents.data_fetcher import _fetch_h4
    mock_dl.return_value = _make_ohlcv_multiindex(n_rows=900)
    result = _fetch_h4()
    assert not isinstance(result.columns, pd.MultiIndex)
    assert set(result.columns) == {"Open", "High", "Low", "Close", "Volume"}


@patch("agents.data_fetcher.yf.download")
def test_fetch_h4_resamples_to_4h(mock_dl):
    from agents.data_fetcher import _fetch_h4
    mock_dl.return_value = _make_ohlcv_multiindex(n_rows=900)
    result = _fetch_h4()
    # After resampling 900 1h bars → 225 4h bars → tail(200)
    assert len(result) == 200


@patch("agents.data_fetcher.yf.download")
def test_fetch_h4_empty_raises(mock_dl):
    from agents.data_fetcher import _fetch_h4
    mock_dl.return_value = pd.DataFrame()
    with pytest.raises(RuntimeError, match="empty H4 data"):
        _fetch_h4()


# ── M15 fetch tests ──────────────────────────────────────────────

@patch("agents.data_fetcher.yf.download")
def test_fetch_m15_flattens_multiindex(mock_dl):
    from agents.data_fetcher import _fetch_m15
    mock_dl.return_value = _make_ohlcv_multiindex(n_rows=300)
    result = _fetch_m15()
    assert not isinstance(result.columns, pd.MultiIndex)
    assert set(result.columns) == {"Open", "High", "Low", "Close", "Volume"}


@patch("agents.data_fetcher.yf.download")
def test_fetch_m15_empty_raises(mock_dl):
    from agents.data_fetcher import _fetch_m15
    mock_dl.return_value = pd.DataFrame()
    with pytest.raises(RuntimeError, match="empty M15 data"):
        _fetch_m15()
