import statistics
import isodate
from datetime import datetime, timedelta, timezone
from src.ai.openai_utils import get_ai_score
import os
from dotenv import load_dotenv

load_dotenv()


class InfluencerMetrics:
    def __init__(self, channel_name, sub_count, video_data, region="Global"):
        self.channel_name = channel_name
        self.sub_count = sub_count
        self.video_data = video_data
        self.region = region

        # ---- Benchmarks (can later be region-based) ----
        self.benchmarks = {
            "engagement_rate": 3.0,
            "like_rate": 2.5,
            "comment_rate": 0.3,
            "loyalty": 10.0,
            "cpm": 40,
        }

    # ---------------- CORE PERFORMANCE METRICS ----------------
    def get_performance_report(self):
        if not self.video_data:
            return {}

        for v in self.video_data:
            v["views"] = int(v.get("views", 0))
            v["likes"] = int(v.get("likes", 0))
            v["comments"] = int(v.get("comments", 0))

        views = [v["views"] for v in self.video_data]
        likes = [v["likes"] for v in self.video_data]
        comments = [v["comments"] for v in self.video_data]

        mean_views = statistics.mean(views)
        median_views = statistics.median(views)
        total_views = sum(views)
        total_likes = sum(likes)
        total_comments = sum(comments)

        engagement_rate = (total_likes + total_comments) / total_views * 100 if total_views else 0
        like_rate = total_likes / total_views * 100 if total_views else 0
        comment_rate = total_comments / total_views * 100 if total_views else 0

        # Engagement consistency (lower = better)
        per_video_engagement = [
            (v["likes"] + v["comments"]) / v["views"] * 100 if v["views"] else 0
            for v in self.video_data
        ]
        engagement_consistency = (
            round(statistics.stdev(per_video_engagement), 2)
            if len(per_video_engagement) > 1 else 0
        )

        # Loyalty
        loyalty_percent = (median_views / self.sub_count * 100) if self.sub_count else 0

        # Risk classification
        volatility_ratio = mean_views / median_views if median_views else 0
        if volatility_ratio > 1.5:
            risk_level = "High (Viral Reliant)"
        elif volatility_ratio > 1.2:
            risk_level = "Moderate"
        else:
            risk_level = "Low (Consistent)"

        # Short vs Long
        short_views, long_views = [], []
        short_count, long_count = 0, 0

        for v in self.video_data:
            try:
                duration = isodate.parse_duration(v["duration"]).total_seconds()
                if duration < 420:
                    short_count += 1
                    short_views.append(v["views"])
                else:
                    long_count += 1
                    long_views.append(v["views"])
            except:
                continue

        short_long_split = {
            "short_count": short_count,
            "long_count": long_count,
            "short_percent": round(short_count / max(short_count + long_count, 1) * 100, 2),
            "short_avg_views": int(statistics.mean(short_views)) if short_views else 0,
            "long_avg_views": int(statistics.mean(long_views)) if long_views else 0,
        }

        # Velocity (last 7 days)
        velocity_views = 0
        now = datetime.now(timezone.utc)

        for v in self.video_data:
            try:
                published = datetime.fromisoformat(v["publishedAt"].replace("Z", "+00:00"))
                if published >= now - timedelta(days=7):
                    velocity_views += v["views"]
            except:
                continue

        velocity_percent = round(velocity_views / total_views * 100, 2) if total_views else 0

        return {
            "mean_views": int(mean_views),
            "median_views": int(median_views),
            "total_views": total_views,
            "risk_level": risk_level,
            "volatility_ratio": round(volatility_ratio, 2),
            "engagement_rate": round(engagement_rate, 2),
            "like_rate": round(like_rate, 2),
            "comment_rate": round(comment_rate, 2),
            "engagement_consistency": engagement_consistency,
            "loyalty_percent": round(loyalty_percent, 2),
            "short_long_split": short_long_split,
            "velocity_views_7d": velocity_views,
            "velocity_percent_7d": velocity_percent,
            "benchmarks": self.benchmarks,
        }

    # ---------------- MONETISATION ----------------
    def calculate_CPM(self, client_cost):
        total_views = sum(v["views"] for v in self.video_data)
        return round(client_cost / max(total_views / 1000, 1), 2)

    def calculate_CPV(self, client_cost):
        total_views = sum(v["views"] for v in self.video_data)
        return round(client_cost / max(total_views, 1), 4)

    def calculate_CPE(self, client_cost):
        total_engagements = sum(v["likes"] + v["comments"] for v in self.video_data)
        return round(client_cost / max(total_engagements, 1), 4)

    def calculate_talent_cost(self, client_cost, agency_margin_percent):
        return round(client_cost * (1 - agency_margin_percent / 100), 2)

    def calculate_engagement_adjusted_CPM(self, client_cost):
        report = self.get_performance_report()
        factor = report["engagement_rate"] / self.benchmarks["engagement_rate"] if self.benchmarks["engagement_rate"] else 1
        return round(self.calculate_CPM(client_cost) * factor, 2)

    # ---------------- DASHBOARD SCORE ----------------
    @property
    def dashboard_score(self):
        r = self.get_performance_report()

        score = (
            0.35 * min(r["engagement_rate"] / self.benchmarks["engagement_rate"], 2) * 50 +
            0.25 * min(r["loyalty_percent"] / self.benchmarks["loyalty"], 2) * 30 +
            0.2 * (100 - min(r["engagement_consistency"] * 10, 100)) +
            0.2 * (50 if r["risk_level"] == "Low (Consistent)" else 30)
        )

        return round(min(score, 100), 2)

    @property
    def dashboard_interpretation(self):
        s = self.dashboard_score
        return (
            "Excellent" if s >= 80 else
            "Good" if s >= 65 else
            "Average" if s >= 45 else
            "Weak"
        )




# """
# Advanced YouTube influencer metrics for performance analysis, monetisation, and AI scoring.
# """

# import statistics
# import isodate
# from datetime import datetime, timedelta, timezone
# from src.ai.openai_utils import get_ai_score
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class InfluencerMetrics:
#     def __init__(self, channel_name, sub_count, video_data, region="Global"):
#         self.channel_name = channel_name
#         self.sub_count = sub_count
#         self.video_data = video_data
#         self.region = region

#     # ---------------- CORE PERFORMANCE METRICS ----------------
#     def get_performance_report(self):
#         if not self.video_data:
#             return None

#         views = [v["views"] for v in self.video_data]
#         likes = [v["likes"] for v in self.video_data]
#         comments = [v["comments"] for v in self.video_data]

#         mean_views = sum(views) / len(views)
#         median_views = statistics.median(views)

#         total_views = sum(views)
#         total_likes = sum(likes)
#         total_comments = sum(comments)

#         engagement_rate = ((total_likes + total_comments) / total_views * 100) if total_views else 0
#         like_rate = (total_likes / total_views * 100) if total_views else 0
#         comment_rate = (total_comments / total_views * 100) if total_views else 0

#         per_video_engagement = [
#             ((v["likes"] + v["comments"]) / v["views"] * 100) if v["views"] else 0
#             for v in self.video_data
#         ]
#         engagement_consistency = (
#             round(statistics.stdev(per_video_engagement), 2)
#             if len(per_video_engagement) > 1 else 0
#         )

#         loyalty_percent = (median_views / self.sub_count * 100) if self.sub_count else 0

#         volatility_ratio = mean_views / median_views if median_views else 0
#         if volatility_ratio > 1.5:
#             risk = "High (Viral Reliant)"
#         elif volatility_ratio > 1.2:
#             risk = "Moderate"
#         else:
#             risk = "Low (Consistent)"

#         short_views, long_views = [], []
#         short_count, long_count = 0, 0

#         for v in self.video_data:
#             try:
#                 duration = isodate.parse_duration(v["duration"]).total_seconds()
#                 if duration < 600:
#                     short_views.append(v["views"])
#                     short_count += 1
#                 else:
#                     long_views.append(v["views"])
#                     long_count += 1
#             except:
#                 continue

#         short_long_split = {
#             "short_form": short_count,
#             "long_form": long_count,
#             "short_form_percent": round(short_count / max(short_count + long_count, 1) * 100, 2),
#             "short_avg_views": int(statistics.mean(short_views)) if short_views else 0,
#             "long_avg_views": int(statistics.mean(long_views)) if long_views else 0
#         }

#         velocity_views = 0
#         now = datetime.now(timezone.utc)
#         for v in self.video_data:
#             try:
#                 published = datetime.fromisoformat(v["publishedAt"].replace("Z", "+00:00"))
#                 if published >= now - timedelta(days=7):
#                     velocity_views += v["views"]
#             except:
#                 continue

#         velocity_percent = round(velocity_views / total_views * 100, 2) if total_views else 0

#         anti_fraud_signals = {
#             "suspicious_view_spike": False,
#             "engagement_too_uniform": engagement_consistency < 0.5,
#             "short_form_overload": short_count / max(short_count + long_count, 1) > 0.9
#         }

#         return {
#             "mean_views": int(mean_views),
#             "median_views": int(median_views),
#             "risk_level": risk,
#             "engagement_rate_percent": round(engagement_rate, 2),
#             "like_rate_percent": round(like_rate, 2),
#             "comment_rate_percent": round(comment_rate, 2),
#             "engagement_consistency_percent": engagement_consistency,
#             "loyalty_percent": round(loyalty_percent, 2),
#             "sample_size": len(self.video_data),
#             "short_long_split": short_long_split,
#             "view_velocity_percent_last_7_days": velocity_percent,
#             "engagement_adjusted_cpm_factor": round(engagement_rate / 100, 2),
#             "anti_fraud_signals": anti_fraud_signals
#         }

#     # ---------------- MONETISATION METRICS (UNCHANGED) ----------------
#     def calculate_CPM(self, client_cost, currency_multiplier=1):
#         total_views = sum(v["views"] for v in self.video_data)
#         return round((client_cost * currency_multiplier) / max(total_views / 1000, 1), 2)

#     def calculate_CPE(self, client_cost, currency_multiplier=1):
#         interactions = sum(v["likes"] + v["comments"] for v in self.video_data)
#         return round((client_cost * currency_multiplier) / max(interactions, 1), 2)

#     def calculate_CPV(self, client_cost, currency_multiplier=1):
#         views = sum(v["views"] for v in self.video_data)
#         return round((client_cost * currency_multiplier) / max(views, 1), 4)

#     def calculate_talent_cost(self, client_cost, agency_margin_percent):
#         return round(client_cost * (1 - agency_margin_percent / 100), 2)

#     def calculate_engagement_adjusted_CPM(self, client_cost, currency_multiplier=1):
#         report = self.get_performance_report()
#         factor = report["engagement_adjusted_cpm_factor"] if report else 0
#         return round(self.calculate_CPM(client_cost, currency_multiplier) * factor, 2)

#     # ---------------- AI ----------------
#     def get_ai_analysis(self):
#         if not hasattr(self, "_ai_cache"):
#             prompt = f"""
#             Analyse the following YouTube influencer metrics for monetisation potential:
#             {self.get_performance_report()}
#             Return JSON with: score (0-100) and summary.
#             """
#             os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#             self._ai_cache = get_ai_score(prompt)
#         return self._ai_cache

#     @property
#     def dashboard_score(self):
#         ai = self.get_ai_analysis()
#         return ai.get("score", 0)

#     @property
#     def dashboard_interpretation(self):
#         s = self.dashboard_score
#         return (
#             "Excellent" if s >= 85 else
#             "Good" if s >= 70 else
#             "Average" if s >= 50 else
#             "Below Average" if s >= 30 else
#             "Poor"
#         )




