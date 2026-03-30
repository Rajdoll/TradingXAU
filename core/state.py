from typing import TypedDict, Optional


class PatternResult(TypedDict):
    name: str                   # e.g. 'Double Bottom'
    win_rate: float             # e.g. 0.93
    direction: str              # 'BUY' | 'SELL'
    formation_pct: float        # 0.0–1.0, how complete the pattern is
    entry_zone_low: float       # lower bound of entry zone price
    entry_zone_high: float      # upper bound of entry zone price
    invalidation_level: float   # price that invalidates the pattern
    tier: int                   # 1 (>80% WR), 2 (65-80%), 3 (<65%)
    skip: bool                  # True for Descending Triangle only


class XAUState(TypedDict):
    # ── Data Layer ──────────────────────────────────────────────
    ohlcv_h4: dict              # pandas DataFrame as dict (H4 OHLCV)
    ohlcv_m15: dict             # pandas DataFrame as dict (M15 OHLCV)
    fetch_timestamp: str        # ISO 8601 UTC
    current_price: float        # Last close on H4
    session: str                # 'LONDON' | 'NEW_YORK' | 'ASIAN'
    news_risk: bool             # High-impact news within 2h
    news_events: list           # List of upcoming event dicts

    # ── Pattern Layer ───────────────────────────────────────────
    patterns_found: list        # List of PatternResult dicts, ranked by WR
    active_pattern: Optional[PatternResult]  # Highest WR pattern
    no_pattern: bool            # True when no pattern detected

    # ── Confirmation Layer ──────────────────────────────────────
    rsi_value: float            # Current RSI(14) on H4
    rsi_signal: str             # 'OVERSOLD' | 'OVERBOUGHT' | 'NEUTRAL'
    candlestick_confirm: bool   # Confirming candle at entry zone
    candlestick_name: str       # e.g. 'Bullish Engulfing'
    sr_context: str             # 'AT_SUPPORT' | 'AT_RESISTANCE' | 'MIDRANGE'
    tech_score: int             # 0-5 weighted confirmation score

    # ── Timeframe Layer ─────────────────────────────────────────
    h4_bias: str                # 'BULLISH' | 'BEARISH' | 'NEUTRAL'
    h4_last_hh: float           # Last Higher High price on H4
    h4_last_hl: float           # Last Higher Low price on H4
    m15_aligned: bool           # M15 entry aligns with H4 bias
    m15_entry_type: str         # 'BREAKOUT' | 'RETEST' | 'PENDING'
    tf_verdict: str             # 'ALIGNED' | 'MISALIGNED' | 'NEUTRAL'

    # ── Macro Layer ─────────────────────────────────────────────
    dxy_trend: str              # 'UP' | 'DOWN' | 'SIDEWAYS'
    tips_yield_direction: str   # 'RISING' | 'FALLING' | 'FLAT'
    macro_bias: str             # 'BULLISH_XAU' | 'BEARISH_XAU' | 'NEUTRAL'
    macro_confidence: str       # 'HIGH' | 'MEDIUM' | 'LOW'

    # ── Debate Layer ────────────────────────────────────────────
    bull_arguments: list        # 3 bull-case argument strings
    bear_arguments: list        # 3 bear-case argument strings
    debate_score: str           # e.g. '4/5 bull'
    debate_verdict: str         # 'STRONG' | 'MODERATE' | 'WEAK'
    debate_key_reason: str      # One-sentence deciding factor

    # ── Risk Layer ──────────────────────────────────────────────
    account_balance: float      # Default: 50.00
    risk_pct: float             # Default: 0.02 (2%)
    risk_usd: float             # Calculated: balance * risk_pct
    lot_size: float             # Always: 0.01 micro lot
    sl_pips: int                # SL distance in pips
    sl_price: float             # Absolute SL price
    tp1_price: float            # Target 1 price (1:1 RR)
    tp2_price: float            # Target 2 price (1:2 RR or Fibo 1.618)
    risk_reward: float          # Actual RR ratio
    risk_approved: bool         # False if any veto rule triggered
    risk_reject_reason: str     # Rejection message if risk_approved=False

    # ── Output Layer ────────────────────────────────────────────
    confidence: str             # 'HIGH' | 'MEDIUM' | 'LOW'
    signal_id: str              # UUID for journal reference
    signal_summary: str         # Formatted signal card string
    journal_written: bool       # True after journal entry created
    pipeline_duration_s: float  # End-to-end runtime in seconds
