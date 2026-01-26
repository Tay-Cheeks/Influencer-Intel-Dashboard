"""
Build a clean, JSON-friendly analysis report for a YouTube creator.

File: src/analysis/analyser.py
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .YT_benchmarks import BENCHMARK_TIERS, get_creator_tier, get_tier_benchmarks


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_range(value: float, rng: Tuple[float, float]) -> str:
    """
    Return 'below' | 'within' | 'above' relative to a (low, high) range.
    """
    low, high = rng
    if value < low:
        return "below"
    if value > high:
        return "above"
    return "within"


def _require_keys(report: Dict[str, Any], keys: list[str]) -> None:
    """
    Validate that required keys exist (even if values are None).
    Raises ValueError with a clean message if missing.
    """
    missing = [k for k in keys if k not in report]
    if missing:
        raise ValueError(
            f"Performance report missing required keys: {', '.join(missing)}"
        )


def build_analysis(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build an analysis layer on top of the raw performance report.

    Expects a 'report' dict produced by your metrics pipeline.
    Returns a JSON-friendly dict for the API + frontend.

    This function is defensive:
    - Raises a clear ValueError if critical keys are missing
    - Uses safe defaults for non-critical/optional fields
    """

    # Critical keys: if these aren't present at all, you're likely calling this too early
    _require_keys(
        report,
        keys=[
            "sub_count",
            "mean_views",
            "median_views",
            "engagement_rate_percent",
            "loyalty_percent",
            "views_per_sub_percent",
        ],
    )

    sub_count = _to_int(report.get("sub_count"))
    mean_views = _to_float(report.get("mean_views"))
    median_views = _to_float(report.get("median_views"))

    engagement_rate_percent = _to_float(report.get("engagement_rate_percent"))
    loyalty_percent = _to_float(report.get("loyalty_percent"))
    views_per_sub_percent = _to_float(report.get("views_per_sub_percent"))

    # Optional fields (safe defaults)
    dashboard_score = _to_float(report.get("dashboard_score"), default=0.0)
    channel_name = report.get("channel_name") or ""
    channel_url = report.get("channel_url") or ""
    short_long_split = report.get("short_long_split") or {"shorts": 0, "long": 0}

    tier = get_creator_tier(sub_count)
    tier_benchmarks = get_tier_benchmarks(tier)

    # Benchmark comparisons
    comparisons = {
        "engagement_rate_percent": {
            "value": engagement_rate_percent,
            "range": tier_benchmarks.get("engagement_rate_percent", (0.0, 0.0)),
        },
        "loyalty_percent": {
            "value": loyalty_percent,
            "range": tier_benchmarks.get("loyalty_percent", (0.0, 0.0)),
        },
        "views_per_sub_percent": {
            "value": views_per_sub_percent,
            "range": tier_benchmarks.get("views_per_sub_percent", (0.0, 0.0)),
        },
    }

    benchmark_positions = {
        metric: _safe_range(_to_float(payload["value"]), payload["range"])
        for metric, payload in comparisons.items()
    }

    # Simple skew flag: if mean is much larger than median, views are spiky.
    viral_skew = False
    if median_views > 0 and mean_views / median_views >= 1.75:
        viral_skew = True

    analysis: Dict[str, Any] = {
        "channel": {
            "name": channel_name,
            "url": channel_url,
            "subscribers": sub_count,
            "tier": tier,
        },
        "rollups": {
            "mean_views": mean_views,
            "median_views": median_views,
            "viral_skew": viral_skew,
            "dashboard_score": dashboard_score,
        },
        "performance": {
            "engagement_rate_percent": engagement_rate_percent,
            "loyalty_percent": loyalty_percent,
            "views_per_sub_percent": views_per_sub_percent,
            "short_long_split": short_long_split,
        },
        "benchmarks": {
            "tier": tier,
            "ranges": tier_benchmarks,
            "positions": benchmark_positions,  # below/within/above per metric
        },
        # Keep the raw input for debugging / transparency (optional, but useful)
        "raw_report": report,
    }

    return analysis
