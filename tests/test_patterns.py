import pytest


# ── Registry structural test ──────────────────────────────────────

def test_pattern_registry_is_list():
    from patterns.base import PATTERN_REGISTRY
    assert isinstance(PATTERN_REGISTRY, list)
