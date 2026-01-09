"""
Advanced YouTube influencer metrics for performance analysis, monetisation, and AI scoring.
"""

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

    # ---------------- CORE PERFORMANCE METRICS ----------------
    def get_performance_report(self):
        if not self.video_data:
            return None

        views = [v["views"] for v in self.video_data]
        likes = [v["likes"] for v in self.video_data]
        comments = [v["comments"] for v in self.video_data]

        mean_views = sum(views) / len(views)
        median_views = statistics.median(views)

        total_views = sum(views)
        total_likes = sum(likes)
        total_comments = sum(comments)

        engagement_rate = ((total_likes + total_comments) / total_views * 100) if total_views else 0
        like_rate = (total_likes / total_views * 100) if total_views else 0
        comment_rate = (total_comments / total_views * 100) if total_views else 0

        per_video_engagement = [
            ((v["likes"] + v["comments"]) / v["views"] * 100) if v["views"] else 0
            for v in self.video_data
        ]
        engagement_consistency = (
            round(statistics.stdev(per_video_engagement), 2)
            if len(per_video_engagement) > 1 else 0
        )

        loyalty_percent = (median_views / self.sub_count * 100) if self.sub_count else 0

        volatility_ratio = mean_views / median_views if median_views else 0
        if volatility_ratio > 1.5:
            risk = "High (Viral Reliant)"
        elif volatility_ratio > 1.2:
            risk = "Moderate"
        else:
            risk = "Low (Consistent)"

        short_views, long_views = [], []
        short_count, long_count = 0, 0

        for v in self.video_data:
            try:
                duration = isodate.parse_duration(v["duration"]).total_seconds()
                if duration < 600:
                    short_views.append(v["views"])
                    short_count += 1
                else:
                    long_views.append(v["views"])
                    long_count += 1
            except:
                continue

        short_long_split = {
            "short_form": short_count,
            "long_form": long_count,
            "short_form_percent": round(short_count / max(short_count + long_count, 1) * 100, 2),
            "short_avg_views": int(statistics.mean(short_views)) if short_views else 0,
            "long_avg_views": int(statistics.mean(long_views)) if long_views else 0
        }

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

        anti_fraud_signals = {
            "suspicious_view_spike": False,
            "engagement_too_uniform": engagement_consistency < 0.5,
            "short_form_overload": short_count / max(short_count + long_count, 1) > 0.9
        }

        return {
            "mean_views": int(mean_views),
            "median_views": int(median_views),
            "risk_level": risk,
            "engagement_rate_percent": round(engagement_rate, 2),
            "like_rate_percent": round(like_rate, 2),
            "comment_rate_percent": round(comment_rate, 2),
            "engagement_consistency_percent": engagement_consistency,
            "loyalty_percent": round(loyalty_percent, 2),
            "sample_size": len(self.video_data),
            "short_long_split": short_long_split,
            "view_velocity_percent_last_7_days": velocity_percent,
            "engagement_adjusted_cpm_factor": round(engagement_rate / 100, 2),
            "anti_fraud_signals": anti_fraud_signals
        }

    # ---------------- MONETISATION METRICS (UNCHANGED) ----------------
    def calculate_CPM(self, client_cost, currency_multiplier=1):
        total_views = sum(v["views"] for v in self.video_data)
        return round((client_cost * currency_multiplier) / max(total_views / 1000, 1), 2)

    def calculate_CPE(self, client_cost, currency_multiplier=1):
        interactions = sum(v["likes"] + v["comments"] for v in self.video_data)
        return round((client_cost * currency_multiplier) / max(interactions, 1), 2)

    def calculate_CPV(self, client_cost, currency_multiplier=1):
        views = sum(v["views"] for v in self.video_data)
        return round((client_cost * currency_multiplier) / max(views, 1), 4)

    def calculate_talent_cost(self, client_cost, agency_margin_percent):
        return round(client_cost * (1 - agency_margin_percent / 100), 2)

    def calculate_engagement_adjusted_CPM(self, client_cost, currency_multiplier=1):
        report = self.get_performance_report()
        factor = report["engagement_adjusted_cpm_factor"] if report else 0
        return round(self.calculate_CPM(client_cost, currency_multiplier) * factor, 2)

    # ---------------- AI ----------------
    def get_ai_analysis(self):
        if not hasattr(self, "_ai_cache"):
            prompt = f"""
            Analyse the following YouTube influencer metrics for monetisation potential:
            {self.get_performance_report()}
            Return JSON with: score (0-100) and summary.
            """
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            self._ai_cache = get_ai_score(prompt)
        return self._ai_cache

    @property
    def dashboard_score(self):
        ai = self.get_ai_analysis()
        return ai.get("score", 0)

    @property
    def dashboard_interpretation(self):
        s = self.dashboard_score
        return (
            "Excellent" if s >= 85 else
            "Good" if s >= 70 else
            "Average" if s >= 50 else
            "Below Average" if s >= 30 else
            "Poor"
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

# # Load .env file to get API keys
# load_dotenv()

# class InfluencerMetrics:
#     def __init__(self, channel_name, sub_count, video_data, region="Global"):
#         """
#         video_data: list of dicts with keys:
#         - views: int
#         - likes: int
#         - comments: int
#         - publishedAt: ISO8601 string
#         - duration: ISO8601 string (e.g. 'PT12M34S')
#         """
#         self.channel_name = channel_name
#         self.sub_count = sub_count
#         self.video_data = video_data
#         self.region = region

#     # ---------------- CORE PERFORMANCE METRICS ----------------
#     def get_performance_report(self):
#         if not self.video_data:
#             return None

#         views_list = [vid["views"] for vid in self.video_data]
#         likes_list = [vid["likes"] for vid in self.video_data]
#         comments_list = [vid["comments"] for vid in self.video_data]

#         mean_views = sum(views_list) / len(views_list)
#         median_views = statistics.median(views_list)

#         total_views = sum(views_list)
#         total_likes = sum(likes_list)
#         total_comments = sum(comments_list)
#         total_interactions = total_likes + total_comments

#         engagement_rate = (total_interactions / total_views * 100) if total_views else 0
#         like_rate = (total_likes / total_views * 100) if total_views else 0
#         comment_rate = (total_comments / total_views * 100) if total_views else 0

#         per_video_engagement = [
#             (vid["likes"] + vid["comments"]) / vid["views"] * 100 if vid["views"] else 0
#             for vid in self.video_data
#         ]
#         engagement_consistency = round(statistics.stdev(per_video_engagement), 2) if len(per_video_engagement) > 1 else 0

#         view_to_sub_ratio = (median_views / self.sub_count * 100) if self.sub_count else 0

#         volatility_ratio = mean_views / median_views if median_views else 0
#         if volatility_ratio > 1.5:
#             risk = "High (Viral Reliant)"
#         elif volatility_ratio > 1.2:
#             risk = "Moderate"
#         else:
#             risk = "Low (Consistent)"

#         short_count, long_count = 0, 0
#         for vid in self.video_data:
#             try:
#                 duration_sec = isodate.parse_duration(vid["duration"]).total_seconds()
#                 if duration_sec < 600:
#                     short_count += 1
#                 else:
#                     long_count += 1
#             except:
#                 continue

#         short_long_split = {
#             "short_form": short_count,
#             "long_form": long_count,
#             "short_form_percent": round(short_count / (short_count + long_count) * 100, 2) if (short_count + long_count) else 0
#         }

#         velocity_views = 0
#         now_utc = datetime.now(timezone.utc)
#         for vid in self.video_data:
#             try:
#                 pub_date = datetime.fromisoformat(vid["publishedAt"].replace("Z", "+00:00"))
#                 if pub_date >= now_utc - timedelta(days=7):
#                     velocity_views += vid["views"]
#             except:
#                 continue
#         velocity_percent = round(velocity_views / total_views * 100, 2) if total_views else 0

#         engagement_adjusted_cpm_factor = engagement_rate / 100

#         anti_fraud_signals = {
#             "suspicious_view_spike": False,
#             "engagement_too_uniform": False,
#             "short_form_overload": short_count / (short_count + long_count) > 0.9 if (short_count + long_count) else False,
#         }

#         return {
#             "mean_views": int(mean_views),
#             "median_views": int(median_views),
#             "risk_level": risk,
#             "engagement_rate_percent": round(engagement_rate, 2),
#             "like_rate_percent": round(like_rate, 2),
#             "comment_rate_percent": round(comment_rate, 2),
#             "engagement_consistency_percent": engagement_consistency,
#             "loyalty_percent": round(view_to_sub_ratio, 2),
#             "sample_size": len(self.video_data),
#             "short_long_split": short_long_split,
#             "view_velocity_percent_last_7_days": velocity_percent,
#             "engagement_adjusted_cpm_factor": round(engagement_adjusted_cpm_factor, 2),
#             "anti_fraud_signals": anti_fraud_signals
#         }

#     # ---------------- MONETISATION METRICS ----------------
#     def calculate_CPM(self, client_cost, currency_multiplier=1):
#         total_views = sum(vid["views"] for vid in self.video_data)
#         if total_views == 0:
#             return 0
#         return round((client_cost * currency_multiplier) / (total_views / 1000), 2)

#     def calculate_CPE(self, client_cost, currency_multiplier=1):
#         total_interactions = sum(vid["likes"] + vid["comments"] for vid in self.video_data)
#         if total_interactions == 0:
#             return 0
#         return round((client_cost * currency_multiplier) / total_interactions, 2)

#     def calculate_CPV(self, client_cost, currency_multiplier=1):
#         total_views = sum(vid["views"] for vid in self.video_data)
#         if total_views == 0:
#             return 0
#         return round((client_cost * currency_multiplier) / total_views, 4)

#     def calculate_talent_cost(self, client_cost, agency_margin_percent):
#         margin_ratio = agency_margin_percent / 100
#         talent_cost = client_cost * (1 - margin_ratio)
#         return round(talent_cost, 2)

#     def calculate_engagement_adjusted_CPM(self, client_cost, currency_multiplier=1):
#         report = self.get_performance_report()
#         factor = report["engagement_adjusted_cpm_factor"] if report else 0
#         return round(self.calculate_CPM(client_cost, currency_multiplier) * factor, 2)

#     # ---------------- AI ANALYSIS & DASHBOARD ----------------
#     def get_ai_analysis(self):
#         if not hasattr(self, "_ai_cache"):
#             report = self.get_performance_report()
#             prompt = f"""
#             You are a YouTube influencer analyst. Given the following metrics for channel "{self.channel_name}":
#             {report}

#             Provide:
#             1. A single influencer performance score from 0 (poor) to 100 (excellent).
#             2. A short text summary highlighting key strengths and risks.
#             Output JSON with keys: "score" and "summary".
#             """
#             # Ensure OpenAI key is loaded from .env
#             os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#             self._ai_cache = get_ai_score(prompt)
#         return self._ai_cache

#     @property
#     def dashboard_score(self):
#         ai_result = self.get_ai_analysis()
#         score = ai_result.get("score", 0)

#         if score == 0:
#             report = self.get_performance_report()
#             if report:
#                 engagement = report.get("engagement_rate_percent", 0)
#                 loyalty = report.get("loyalty_percent", 0)
#                 consistency = max(0, 100 - report.get("engagement_consistency_percent", 0)*10)
#                 score = round(min(max(0.4*engagement + 0.3*loyalty + 0.3*consistency, 0), 100), 2)
#         return score

#     @property
#     def dashboard_interpretation(self):
#         score = self.dashboard_score
#         if score >= 85:
#             return "Excellent"
#         elif score >= 70:
#             return "Good"
#         elif score >= 50:
#             return "Average"
#         elif score >= 30:
#             return "Below Average"
#         else:
#             return "Poor"


