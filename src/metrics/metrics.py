"""
Advanced YouTube influencer metrics for performance analysis, monetisation, and AI scoring.
"""

import statistics
import isodate
from datetime import datetime, timedelta, timezone
import os

class InfluencerMetrics:
    def __init__(self, channel_name, sub_count, video_data, region="Global"):
        """
        video_data: list of dicts with keys:
        - views: int
        - likes: int
        - comments: int
        - publishedAt: ISO8601 string
        - duration: ISO8601 string (e.g. 'PT12M34S')
        """
        self.channel_name = channel_name
        self.sub_count = sub_count
        self.video_data = video_data
        self.region = region

    #CORE PERFORMANCE METRICS
    def get_performance_report(self):
        if not self.video_data:
            return None

        views_list = [vid["views"] for vid in self.video_data]
        likes_list = [vid["likes"] for vid in self.video_data]
        comments_list = [vid["comments"] for vid in self.video_data]

        mean_views = sum(views_list) / len(views_list)
        median_views = statistics.median(views_list)

        #Engagement
        total_views = sum(views_list)
        total_likes = sum(likes_list)
        total_comments = sum(comments_list)
        total_interactions = total_likes + total_comments

        engagement_rate = (total_interactions / total_views * 100) if total_views else 0
        like_rate = (total_likes / total_views * 100) if total_views else 0
        comment_rate = (total_comments / total_views * 100) if total_views else 0

        #Engagement consistency (std dev of engagement rates per video)
        per_video_engagement = [
            (vid["likes"] + vid["comments"]) / vid["views"] * 100 if vid["views"] else 0
            for v in self.video_data
        ]
        engagement_consistency = round(statistics.stdev(per_video_engagement), 2) if len(per_video_engagement) > 1 else 0

        # View-to-subscriber ratio
        view_to_sub_ratio = (median_views / self.sub_count * 100) if self.sub_count else 0

        # Risk / Volatility
        volatility_ratio = mean_views / median_views if median_views else 0
        if volatility_ratio > 1.5:
            risk = "High (Viral Reliant)"
        elif volatility_ratio > 1.2:
            risk = "Moderate"
        else:
            risk = "Low (Consistent)"

        # Short vs Long form
        short_count, long_count = 0, 0
        for v in self.video_data:
            try:
                duration_sec = isodate.parse_duration(v["duration"]).total_seconds()
                if duration_sec < 600:
                    short_count += 1
                else:
                    long_count += 1
            except:
                continue

        short_long_split = {
            "short_form": short_count,
            "long_form": long_count,
            "short_form_percent": round(short_count / (short_count + long_count) * 100, 2) if (short_count + long_count) else 0
        }

        # View velocity (first 7 days)
        velocity_views = 0
        now_utc = datetime.now(timezone.utc)
        for v in self.video_data:
            try:
                pub_date = datetime.fromisoformat(v["publishedAt"].replace("Z", "+00:00"))
                if pub_date >= now_utc - timedelta(days=7):
                    velocity_views += v["views"]
            except:
                continue
        velocity_percent = round(velocity_views / total_views * 100, 2) if total_views else 0

        # Engagement-adjusted CPM factor placeholder
        engagement_adjusted_cpm_factor = engagement_rate / 100

        # Placeholder anti-fraud signals
        anti_fraud_signals = {
            "suspicious_view_spike": False,
            "engagement_too_uniform": False,
            "short_form_overload": short_count / (short_count + long_count) > 0.9 if (short_count + long_count) else False,
        }

        return {
            "mean_views": int(mean_views),
            "median_views": int(median_views),
            "risk_level": risk,
            "engagement_rate_percent": round(engagement_rate, 2),
            "like_rate_percent": round(like_rate, 2),
            "comment_rate_percent": round(comment_rate, 2),
            "engagement_consistency_percent": engagement_consistency,
            "loyalty_percent": round(view_to_sub_ratio, 2),
            "sample_size": len(self.video_data),
            "short_long_split": short_long_split,
            "view_velocity_percent_last_7_days": velocity_percent,
            "engagement_adjusted_cpm_factor": round(engagement_adjusted_cpm_factor, 2),
            "anti_fraud_signals": anti_fraud_signals
        }

    # -----------------------------
    # Monetization Metrics
    # -----------------------------
    def calculate_CPM(self, client_cost, currency_multiplier=1):
        total_views = sum(v["views"] for v in self.video_data)
        if total_views == 0:
            return 0
        return round((client_cost * currency_multiplier) / (total_views / 1000), 2)

    def calculate_CPE(self, client_cost, currency_multiplier=1):
        total_interactions = sum(v["likes"] + v["comments"] for v in self.video_data)
        if total_interactions == 0:
            return 0
        return round((client_cost * currency_multiplier) / total_interactions, 2)

    def calculate_CPV(self, client_cost, currency_multiplier=1):
        total_views = sum(v["views"] for v in self.video_data)
        if total_views == 0:
            return 0
        return round((client_cost * currency_multiplier) / total_views, 4)

    def calculate_talent_cost(self, client_cost, agency_margin_percent):
        margin_ratio = agency_margin_percent / 100
        talent_cost = client_cost * (1 - margin_ratio)
        return round(talent_cost, 2)

    def calculate_engagement_adjusted_CPM(self, client_cost, currency_multiplier=1):
        """CPM scaled by engagement rate"""
        report = self.get_performance_report()
        factor = report["engagement_adjusted_cpm_factor"] if report else 0
        return round(self.calculate_CPM(client_cost, currency_multiplier) * factor, 2)
