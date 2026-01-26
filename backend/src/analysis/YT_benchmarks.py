"""
YouTube creator benchmarks & tiering.

File: src/analysis/YT_benchmarks.py
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

# Tiers are evaluated top-down by subscriber threshold.
# You can adjust these whenever you calibrate your model.
BENCHMARK_TIERS: Dict[str, Dict[str, Any]] = {
    # >= 1M subs
    "mega": {
        "min_subs": 1_000_000,
        "benchmarks": {
            "engagement_rate_percent": (2.0, 6.0),
            "loyalty_percent": (1.5, 5.0),
            "views_per_sub_percent": (2.0, 10.0),
        },
    },
    # >= 100k subs
    "macro": {
        "min_subs": 100_000,
        "benchmarks": {
            "engagement_rate_percent": (2.5, 7.0),
            "loyalty_percent": (2.0, 6.0),
            "views_per_sub_percent": (3.0, 15.0),
        },
    },
    # >= 10k subs
    "micro": {
        "min_subs": 10_000,
        "benchmarks": {
            "engagement_rate_percent": (3.0, 8.0),
            "loyalty_percent": (2.5, 7.0),
            "views_per_sub_percent": (5.0, 25.0),
        },
    },
    # >= 1k subs
    "nano": {
        "min_subs": 1_000,
        "benchmarks": {
            "engagement_rate_percent": (3.5, 10.0),
            "loyalty_percent": (3.0, 8.0),
            "views_per_sub_percent": (8.0, 35.0),
        },
    },
    # < 1k subs (new)
    "tiny": {
        "min_subs": 0,
        "benchmarks": {
            "engagement_rate_percent": (4.0, 12.0),
            "loyalty_percent": (3.5, 10.0),
            "views_per_sub_percent": (10.0, 50.0),
        },
    },
}


def get_creator_tier(subscribers: int | float | None) -> str:
    """
    Return a tier label based on subscriber count.

    - Handles None/invalid values gracefully by returning "tiny".
    - Evaluates tiers top-down by min_subs.
    """
    try:
        subs = int(subscribers or 0)
    except (TypeError, ValueError):
        subs = 0

    # Sort by min_subs desc so the first match is the highest tier.
    tiers_sorted = sorted(
        BENCHMARK_TIERS.items(),
        key=lambda kv: int(kv[1].get("min_subs", 0)),
        reverse=True,
    )

    for tier_name, tier_cfg in tiers_sorted:
        min_subs = int(tier_cfg.get("min_subs", 0))
        if subs >= min_subs:
            return tier_name

    return "tiny"


def get_tier_benchmarks(tier: str) -> Dict[str, Tuple[float, float]]:
    """
    Get the benchmark ranges for a tier.
    If tier unknown, defaults to "tiny".
    """
    cfg = BENCHMARK_TIERS.get(tier) or BENCHMARK_TIERS["tiny"]
    benchmarks = cfg.get("benchmarks", {})
    # Ensure tuples of floats for consistent downstream use
    cleaned: Dict[str, Tuple[float, float]] = {}
    for k, v in benchmarks.items():
        try:
            lo, hi = v
            cleaned[k] = (float(lo), float(hi))
        except Exception:
            # If malformed, skip rather than crash
            continue
    return cleaned
