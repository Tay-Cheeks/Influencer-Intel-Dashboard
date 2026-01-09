# src/analysis/analyzer.py

from .YT_benchmarks import BENCHMARK_TIERS
from .YT_benchmarks import get_creator_tier

def build_analysis(metrics):
    report = metrics.get_performance_report() #dependency inversion
    tier = get_creator_tier(metrics.sub_count)
    benchmark = BENCHMARK_TIERS[tier]

    mean_views = report["mean_views"]
    median_views = report["median_views"]

    # Mean vs Median logic
    if abs(mean_views - median_views) / max(median_views, 1) < 0.15:
        distribution = "Stable"
        dist_expl = "Views are evenly distributed, indicating consistent performance."
    elif mean_views > median_views:
        distribution = "Outlier-Driven"
        dist_expl = "Performance relies on high-performing videos."
    else:
        distribution = "Declining"
        dist_expl = "Recent videos underperform historical averages."

    # Engagement benchmarking
    er = report["engagement_rate_percent"]
    er_low, er_high = benchmark["engagement_rate"]
    if er > er_high:
        er_pos = "Above"
    elif er < er_low:
        er_pos = "Below"
    else:
        er_pos = "Within"

    # Loyalty benchmarking
    loyalty = report["loyalty_percent"]
    l_low, l_high = benchmark["loyalty_percent"]
    if loyalty > l_high:
        loyalty_pos = "Above"
    elif loyalty < l_low:
        loyalty_pos = "Below"
    else:
        loyalty_pos = "Within"

    return {
        "overview": {
            "channel_name": metrics.channel_name,
            "sample_size": report["sample_size"],
            "dashboard_score": metrics.dashboard_score,
            "performance_label": metrics.dashboard_interpretation,
        },

        "distribution_analysis": {
            "mean_views": mean_views,
            "median_views": median_views,
            "distribution_type": distribution,
            "explanation": dist_expl,
        },

        "engagement_analysis": {
            "engagement_rate_percent": er,
            "like_rate_percent": report["like_rate_percent"],
            "comment_rate_percent": report["comment_rate_percent"],
            "consistency": report["engagement_consistency_percent"],
            "quality_label": (
                "High" if er > 6 else "Moderate" if er > 3 else "Low"
            ),
        },

        "audience_quality": {
            "loyalty_percent": loyalty,
            "strength": (
                "Strong" if loyalty > l_high else
                "Moderate" if loyalty >= l_low else
                "Weak"
            ),
        },

        "content_strategy": {
            "short_form_percent": report["short_long_split"]["short_form_percent"],
            "velocity_percent_last_7_days": report["view_velocity_percent_last_7_days"],
            "momentum": (
                "Growing" if report["view_velocity_percent_last_7_days"] > 40
                else "Stable"
            ),
        },

        "risk_assessment": {
            "risk_level": report["risk_level"],
            "anti_fraud_flags": report["anti_fraud_signals"],
        },

        "benchmark_positioning": {
            "tier": tier,
            "engagement_vs_benchmark": er_pos,
            "loyalty_vs_benchmark": loyalty_pos,
            "overall_positioning": (
                "Strong" if er_pos == "Above" and loyalty_pos != "Below"
                else "Competitive" if er_pos != "Below"
                else "Weak"
            ),
        }
    }
