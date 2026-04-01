# patterns/base.py
# Shared interface for all pattern detectors.
# Each pattern module appends its detector to PATTERN_REGISTRY at import time.
# pattern_scanner (Task 1.8) imports each pattern module to trigger registration,
# then iterates PATTERN_REGISTRY to collect non-None results.
#
# All detector functions share this signature:
#   detect_X(df: pd.DataFrame, swings: SwingPoints, current_price: float) -> Optional[PatternResult]
#
# Registry is ordered by win rate descending (Tier 1 first).
PATTERN_REGISTRY: list = []
