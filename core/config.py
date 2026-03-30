import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM Models ──────────────────────────────────────────────────
ANALYST_MODEL = os.getenv("ANALYST_MODEL", "claude-sonnet-4-6")
LIGHT_MODEL   = os.getenv("LIGHT_MODEL",   "claude-haiku-4-5-20251001")

# ── API Keys ─────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
FRED_API_KEY      = os.getenv("FRED_API_KEY", "")

# ── Risk Parameters (PRD §9 — INVARIANT for $50 account) ────────
# ACCOUNT_BALANCE and RISK_PCT are env-overridable (python main.py config --balance N)
# All other risk values are hardcoded and must not be changed without
# explicit account upgrade justification per PRD §9.
ACCOUNT_BALANCE   = float(os.getenv("ACCOUNT_BALANCE", "50.00"))
RISK_PCT          = float(os.getenv("RISK_PCT",        "0.02"))
RISK_USD          = ACCOUNT_BALANCE * RISK_PCT  # = $1.00 at defaults
LOT_SIZE          = 0.01    # Micro lot — always fixed
PIP_VALUE         = 0.01    # $0.01 per pip at 0.01 lot on XAU/USD
MAX_SL_PIPS       = 100     # 100 × $0.01 = $1.00 = 2% of $50
MIN_SL_PIPS       = 15      # Below this = spread erosion risk
SL_BUFFER_PIPS    = 20      # Add beyond pattern invalidation level
MIN_RR            = 2.0     # Minimum 1:2 risk:reward per Astronacci
MAX_DAILY_LOSSES  = 2       # Pause trading after N consecutive losses today
NEWS_BUFFER_HOURS = 2       # Hours before high-impact news to stand aside

# ── Data Config ──────────────────────────────────────────────────
TICKER        = "GC=F"  # Gold Futures — proxy for XAU/USD spot
H4_BARS       = 200     # H4 candles to fetch (≈33 trading days)
M15_BARS      = 200     # M15 candles to fetch (≈2 trading days)
SWING_WINDOW  = 5       # argrelextrema order for pivot point detection
