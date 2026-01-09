import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta, timezone
from src.metrics.metrics import InfluencerMetrics
from src.analysis.analyser import build_analysis

st.set_page_config(page_title="Influencer Intel Dashboard", layout="wide")
st.title("Influencer Intel Dashboard")

# ---------------- Sidebar Inputs ----------------
st.sidebar.header("Creator & Settings")
creator_url = st.sidebar.text_input("Enter YouTube channel URL or name")
region = st.sidebar.selectbox("Region", ["Global", "South Africa", "USA", "UK", "Germany", "Other"])
currency = st.sidebar.selectbox("Currency", ["ZAR", "USD", "EUR", "GBP"])

client_cost = st.sidebar.number_input(f"Client Cost ({currency})", min_value=0.0, value=500.0, step=50.0)
agency_margin = st.sidebar.number_input("Agency Margin (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)

timeframe = st.sidebar.radio("Video Stats Timeframe", ["Daily (last 30 days)", "Weekly (last 4 weeks)"])

# ---------------- Metrics Fetching ----------------
@st.cache_data(ttl=86400)  # cache for 24 hours
def get_metrics(url, region):
    # Placeholder: Replace with YouTube API call to fetch latest video data
    today = datetime.now(timezone.utc)
    sample_videos = []
    for i in range(10):
        sample_videos.append({
            "views": 2000 + i*50,
            "likes": 180 + i*5,
            "comments": 20 + i,
            "publishedAt": (today - timedelta(days=i*3)).isoformat(),
            "duration": "PT12M34S" if i % 2 == 0 else "PT5M0S"
        })
    sub_count = 10000
    metrics = InfluencerMetrics(
        channel_name=url,
        sub_count=sub_count,
        video_data=sample_videos,
        region=region
    )
    return metrics

if creator_url:
    try:
        metrics = get_metrics(creator_url, region)
        talent_cost = metrics.calculate_talent_cost(client_cost, agency_margin)
        analysis = build_analysis(metrics)

        # ---------------- Overview ----------------
        st.subheader("Overview")
        st.write(analysis["overview"])

        # ---------------- Video Stats ----------------
        st.subheader(f"{timeframe} Video Stats")
        df = pd.DataFrame(metrics.video_data)
        df["publishedAt"] = pd.to_datetime(df["publishedAt"])
        df = df.sort_values("publishedAt")

        if timeframe.startswith("Weekly"):
            df["week"] = df["publishedAt"].dt.to_period("W").apply(lambda r: r.start_time)
            df_grouped = df.groupby("week")[["views", "likes", "comments"]].sum().reset_index()
            df_chart = df_grouped.melt(id_vars=["week"], value_vars=["views", "likes", "comments"],
                                       var_name="Metric", value_name="Count")
            x_axis = "week:T"
        else:
            df_chart = df.melt(id_vars=["publishedAt"], value_vars=["views", "likes", "comments"],
                               var_name="Metric", value_name="Count")
            x_axis = "publishedAt:T"

        chart = alt.Chart(df_chart).mark_line(point=True).encode(
            x=x_axis,
            y="Count:Q",
            color="Metric:N",
            tooltip=[x_axis, "Metric:N", "Count:Q"]
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

        # ---------------- Performance Distribution ----------------
        st.subheader("Performance Distribution")
        st.write(analysis["distribution_analysis"])

        # ---------------- Engagement ----------------
        st.subheader("Engagement Metrics")
        df_engagement = pd.DataFrame({
            "Metric": ["Engagement Rate", "Like Rate", "Comment Rate"],
            "Percent": [
                analysis["engagement_analysis"]["engagement_rate_percent"],
                analysis["engagement_analysis"]["like_rate_percent"],
                analysis["engagement_analysis"]["comment_rate_percent"]
            ]
        })
        engagement_chart = alt.Chart(df_engagement).mark_bar().encode(
            x='Metric',
            y='Percent',
            tooltip=['Metric', 'Percent']
        )
        st.altair_chart(engagement_chart, use_container_width=True)
        st.write(analysis["engagement_analysis"])

        # ---------------- Audience Quality ----------------
        st.subheader("Audience Quality")
        st.write(analysis["audience_quality"])

        # ---------------- Risk Assessment ----------------
        st.subheader("Risk Assessment")
        st.write(analysis["risk_assessment"])

        # ---------------- Benchmark Positioning ----------------
        st.subheader("Benchmark Positioning")
        st.write(analysis["benchmark_positioning"])

        # ---------------- Monetisation ----------------
        st.subheader("Monetisation Metrics")
        monetisation = {
            "Client Cost": f"{client_cost} {currency}",
            "Agency Margin (%)": agency_margin,
            "Talent Cost": f"{talent_cost} {currency}",
            "CPM": metrics.calculate_CPM(talent_cost),
            "CPE": metrics.calculate_CPE(talent_cost),
            "CPV": metrics.calculate_CPV(talent_cost),
            "Engagement-Adjusted CPM": metrics.calculate_engagement_adjusted_CPM(talent_cost)
        }
        st.write(monetisation)

    except Exception as e:
        st.error(f"Failed to load metrics: {e}")







# import streamlit as st
# import altair as alt
# import pandas as pd
# from datetime import datetime

# import sys
# import os

# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


# from src.metrics.metrics import InfluencerMetrics
# from src.analysis.analyser import build_analysis

# # ---------------------------
# # Streamlit config
# # ---------------------------
# st.set_page_config(
#     page_title="Creator Performance Dashboard",
#     layout="wide"
# )

# st.title("🎯 Creator Performance & Monetisation Dashboard")
# st.caption("Data-driven influencer analysis for brand & talent decisions")

# # ---------------------------
# # Sidebar – Inputs for Emma
# # ---------------------------
# st.sidebar.header("🔗 Creator Input")

# creator_url = st.sidebar.text_input(
#     "YouTube Channel or Video URL",
#     placeholder="https://www.youtube.com/@creator"
# )

# talent_cost = st.sidebar.number_input(
#     "Talent Cost (ZAR)",
#     min_value=0.0,
#     value=400.0,
#     step=50.0
# )

# region = st.sidebar.selectbox(
#     "Primary Audience Region",
#     ["South Africa", "Global", "US", "EU"]
# )

# run_analysis = st.sidebar.button("Run Analysis")

# # ---------------------------
# # Cached data fetch (daily)
# # ---------------------------
# @st.cache_data(ttl=86400)  # 24 hours
# def get_metrics(url, talent_cost, region):
#     """
#     Fetch creator data + compute metrics.
#     TTL ensures daily refresh.
#     """

#     # TODO: replace this stub with real YouTube API data
#     video_data = [
#         {"views": 2200, "likes": 210, "comments": 30, "days_since_posted": 2},
#         {"views": 1800, "likes": 160, "comments": 18, "days_since_posted": 6},
#         {"views": 2000, "likes": 180, "comments": 20, "days_since_posted": 10},
#     ]

#     metrics = InfluencerMetrics(
#         channel_name=url,
#         subscribers=12000,
#         video_data=video_data,
#         region=region,
#         talent_cost=talent_cost
#     )

#     return metrics


# # ---------------------------
# # Run analysis
# # ---------------------------
# if run_analysis and creator_url:

#     metrics = get_metrics(creator_url, talent_cost, region)
#     analysis = build_analysis(metrics)

#     report = metrics.get_performance_report()
#     monetisation = metrics.get_monetisation_metrics()

#     # ---------------------------
#     # KPI Row
#     # ---------------------------
#     st.subheader("📊 Key Performance Indicators")

#     kpi1, kpi2, kpi3, kpi4 = st.columns(4)

#     kpi1.metric("Mean Views", report["mean_views"])
#     kpi2.metric("Median Views", report["median_views"])
#     kpi3.metric("Engagement Rate", f'{report["engagement_rate_percent"]}%')
#     kpi4.metric("Dashboard Score", f'{analysis["dashboard_score"]:.1f}')

#     # ---------------------------
#     # Mean vs Median Analysis
#     # ---------------------------
#     st.subheader("📈 View Distribution Health")

#     view_df = pd.DataFrame({
#         "Metric": ["Mean Views", "Median Views"],
#         "Views": [report["mean_views"], report["median_views"]]
#     })

#     bar_chart = alt.Chart(view_df).mark_bar().encode(
#         x="Metric",
#         y="Views",
#         color="Metric"
#     )

#     st.altair_chart(bar_chart, use_container_width=True)

#     if report["mean_views"] < report["median_views"]:
#         st.info(
#             "Median views are higher than mean views. "
#             "This indicates **stable performance without heavy spikes**."
#         )
#     else:
#         st.warning(
#             "Mean views exceed median views. "
#             "Performance may be driven by a few viral videos."
#         )

#     # ---------------------------
#     # Engagement Breakdown
#     # ---------------------------
#     st.subheader("💬 Engagement Composition")

#     engagement_df = pd.DataFrame({
#         "Type": ["Likes", "Comments"],
#         "Rate (%)": [
#             report["like_rate_percent"],
#             report["comment_rate_percent"]
#         ]
#     })

#     pie_chart = alt.Chart(engagement_df).mark_arc().encode(
#         theta="Rate (%)",
#         color="Type"
#     )

#     st.altair_chart(pie_chart, use_container_width=True)

#     # ---------------------------
#     # Consistency & Risk
#     # ---------------------------
#     st.subheader("⚠️ Risk & Consistency Signals")

#     st.write(f"**Risk Level:** {report['risk_level']}")
#     st.write("**Anti-Fraud Checks:**")

#     for signal, value in report["anti_fraud_signals"].items():
#         if value:
#             st.error(f"⚠️ {signal.replace('_', ' ').title()}")
#         else:
#             st.success(f"✓ {signal.replace('_', ' ').title()}")

#     # ---------------------------
#     # Monetisation Metrics
#     # ---------------------------
#     st.subheader("💰 Monetisation Snapshot")

#     m1, m2, m3, m4 = st.columns(4)

#     m1.metric("CPM", f"R{monetisation['cpm']}")
#     m2.metric("CPE", f"R{monetisation['cpe']}")
#     m3.metric("CPV", f"R{monetisation['cpv']}")
#     m4.metric("Adj. CPM", f"R{monetisation['engagement_adjusted_cpm']}")

#     # ---------------------------
#     # Final Recommendation
#     # ---------------------------
#     st.subheader("🧠 Analyst Summary")

#     st.markdown(f"""
#     **Overall Rating:** {analysis["interpretation"]}

#     **Why this matters for Emma:**
#     - Consistency score suggests **predictable delivery**
#     - Engagement sits **above benchmark**
#     - Cost efficiency is **acceptable for branded campaigns**
#     """)

#     st.caption(f"Last refreshed: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
