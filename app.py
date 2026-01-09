import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

from src.youtube.client import get_channel_stats, get_recent_videos
from src.metrics.metrics import InfluencerMetrics
from src.analysis.analyser import build_analysis

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(
    page_title="Influencer Intel Dashboard",
    layout="wide"
)

st.title("Influencer Intel Dashboard")
st.caption("Data-driven influencer performance, engagement & monetisation analysis")

# ---------------- SIDEBAR INPUTS ----------------
with st.sidebar:
    st.header("Channel Input")

    creator_url = st.text_input(
        "YouTube Channel URL or Handle",
        placeholder="https://youtube.com/@creator"
    )

    st.divider()
    st.header("Campaign Inputs")

    client_cost = st.number_input(
        "Client Cost",
        min_value=0.0,
        step=100.0
    )

    agency_margin = st.slider(
        "Agency Margin (%)",
        min_value=0,
        max_value=50,
        value=20
    )

    run_btn = st.button("Run Analysis", type="primary")

# ---------------- MAIN LOGIC ----------------
if run_btn and creator_url:

    with st.spinner("Fetching YouTube data..."):
        channel = get_channel_stats(creator_url)

        if not channel:
            st.error("Could not fetch channel data.")
            st.stop()

        videos = get_recent_videos(channel["uploads_playlist_id"], count=8)

        if not videos:
            st.error("No recent videos found.")
            st.stop()

    metrics = InfluencerMetrics(
        channel_name=channel["channel_name"],
        sub_count=channel["subscribers"],
        video_data=videos,
        region=channel["region"]
    )

    report = metrics.get_performance_report()
    analysis = build_analysis(metrics)

    talent_cost = metrics.calculate_talent_cost(client_cost, agency_margin)

    # ---------------- TOP SUMMARY ----------------
    st.subheader(channel["channel_name"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Subscribers", f"{channel['subscribers']:,}")
    col2.metric("Average Views (8 videos)", f"{report['mean_views']:,}")
    col3.metric("Median Views", f"{report['median_views']:,}")
    col4.metric(
        "Dashboard Score",
        f"{analysis['overview']['dashboard_score']}",
        analysis["overview"]["performance_label"]
    )

    st.divider()

    # ---------------- DATAFRAME ----------------
    df = pd.DataFrame(videos)

    # Defensive guards
    required_cols = {"title", "publishedAt", "views", "likes", "comments", "duration"}
    if not required_cols.issubset(df.columns):
        st.error("Video data missing required fields.")
        st.stop()

    df["published_date"] = pd.to_datetime(df["publishedAt"])
    df["label"] = df["title"] + " (" + df["published_date"].dt.strftime("%Y-%m-%d") + ")"

    # ---------------- VIEWS BAR CHART (ALTAIR) ----------------
    st.subheader("Views per Recent Video")

    views_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("label:N", sort="-y", title="Video"),
            y=alt.Y("views:Q", title="Views"),
            tooltip=["title", "views"]
        )
        .properties(height=350)
    )

    st.altair_chart(views_chart, use_container_width=True)

    st.caption(
        "This chart shows views for the creator’s most recent 8 uploads. "
        "Average and median views are calculated from this same dataset."
    )

    st.divider()

    # ---------------- ENGAGEMENT CHART ----------------
    st.subheader("Engagement Breakdown")

    engagement_df = df.melt(
        id_vars=["label"],
        value_vars=["likes", "comments"],
        var_name="Type",
        value_name="Count"
    )

    engagement_chart = (
        alt.Chart(engagement_df)
        .mark_bar()
        .encode(
            x=alt.X("label:N", title="Video"),
            y=alt.Y("Count:Q"),
            color="Type:N",
            tooltip=["Type", "Count"]
        )
        .properties(height=350)
    )

    st.altair_chart(engagement_chart, use_container_width=True)

    st.caption(
        "Likes and comments per video help assess engagement quality, not just reach."
    )

    st.divider()

    # ---------------- SHORTS VS LONG FORM ----------------
    st.subheader("Content Format Mix")

    sl = report["short_long_split"]
    sl_df = pd.DataFrame({
        "Format": ["Short-form", "Long-form"],
        "Count": [sl["short_form"], sl["long_form"]]
    })

    format_chart = (
        alt.Chart(sl_df)
        .mark_arc()
        .encode(
            theta="Count:Q",
            color="Format:N",
            tooltip=["Format", "Count"]
        )
        .properties(height=300)
    )

    st.altair_chart(format_chart, use_container_width=True)

    st.caption(
        "A heavy short-form skew may inflate views but reduce depth and conversion."
    )

    st.divider()

    # ---------------- ANALYSIS SECTION ----------------
    st.subheader("Performance Analysis")

    dist = analysis["distribution_analysis"]
    st.markdown(
        f"""
        **View Distribution:** {dist['distribution_type']}  
        {dist['explanation']}
        """
    )

    eng = analysis["engagement_analysis"]
    st.markdown(
        f"""
        **Engagement Rate:** {eng['engagement_rate_percent']}%  
        This reflects how actively viewers interact relative to total views.
        """
    )

    aud = analysis["audience_quality"]
    st.markdown(
        f"""
        **Audience Loyalty:** {aud['loyalty_percent']}%  
        Indicates how much of the subscriber base watches new uploads.
        """
    )

    risk = analysis["risk_assessment"]
    st.markdown(
        f"""
        **Risk Level:** {risk['risk_level']}  
        Based on volatility and reliance on viral spikes.
        """
    )

    st.divider()

    # ---------------- MONETISATION ----------------
    st.subheader("Monetisation Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Client Cost", f"{client_cost:,.2f}")
    col2.metric("Talent Cost", f"{talent_cost:,.2f}")
    col3.metric("CPM", metrics.calculate_CPM(client_cost))
    col4.metric("Engagement-Adjusted CPM", metrics.calculate_engagement_adjusted_CPM(client_cost))

    st.caption(
        "Engagement-adjusted CPM discounts inflated reach and rewards genuine interaction."
    )

    st.divider()

    # ---------------- AI SUMMARY ----------------
    with st.expander("AI Performance Summary"):
        ai = metrics.get_ai_analysis()
        st.write(ai.get("summary", "AI analysis unavailable."))

else:
    st.info("Enter a YouTube channel and campaign details to begin.")





# import streamlit as st
# import pandas as pd
# import altair as alt
# from src.metrics.metrics import InfluencerMetrics
# from src.analysis.analyser import build_analysis
# from src.youtube.client import get_channel_stats, get_recent_videos

# # ---------- App Config ----------
# st.set_page_config(page_title="Influencer Intel Dashboard", layout="wide")
# st.title("Influencer Intel Dashboard")
# st.write("Analyze YouTube influencer performance and monetisation metrics.")

# # ---------- Input ----------
# creator_input = st.text_input("YouTube Channel URL / Handle / ID")
# client_cost = st.number_input("Client Cost (in your currency)", min_value=0.0, step=1.0)
# agency_margin = st.number_input("Agency Margin %", min_value=0.0, max_value=100.0, step=1.0)

# # ---------- Fetch & Process Data ----------
# @st.cache_data(ttl=3600)
# def get_metrics(creator_input, client_cost, agency_margin):
#     # Step 1: Fetch channel stats
#     channel_stats = get_channel_stats(creator_input)
#     if not channel_stats:
#         return None

#     sub_count = channel_stats["subscribers"]
#     playlist_id = channel_stats["uploads_playlist_id"]
#     region = channel_stats["region"]

#     # Step 2: Fetch recent videos
#     video_data = get_recent_videos(playlist_id, count=8)
#     if not video_data:
#         return None

#     # Step 3: Create InfluencerMetrics instance
#     metrics = InfluencerMetrics(
#         channel_name=channel_stats["channel_name"],
#         sub_count=sub_count,
#         video_data=video_data,
#         region=region
#     )

#     # Step 4: Calculate talent cost
#     talent_cost = metrics.calculate_talent_cost(client_cost, agency_margin)

#     # Step 5: Build analysis
#     analysis_report = build_analysis(metrics)

#     # Add monetisation info
#     analysis_report["monetisation"] = {
#         "client_cost": client_cost,
#         "agency_margin_percent": agency_margin,
#         "talent_cost": talent_cost,
#         "avg_views_recent": round(sum(v["views"] for v in video_data)/len(video_data), 2),
#         "median_views_recent": round(pd.Series([v["views"] for v in video_data]).median(), 2)
#     }

#     # Add video data for charts
#     # Calculate view-to-sub ratio for each video
#     for v in video_data:
#         v["view_to_sub_ratio"] = round((v["views"] / sub_count * 100) if sub_count else 0, 2)
#         v["engagement_rate"] = round(((v["likes"] + v["comments"]) / v["views"] * 100) if v["views"] else 0, 2)

#     analysis_report["video_data"] = video_data

#     return analysis_report

# # ---------- Main ----------
# if creator_input:
#     with st.spinner("Fetching metrics..."):
#         metrics = get_metrics(creator_input, client_cost, agency_margin)

#     if metrics:
#         st.subheader("Channel Overview")
#         st.write(metrics["overview"])

#         st.subheader("Distribution Analysis")
#         st.write(metrics["distribution_analysis"])

#         st.subheader("Engagement Analysis")
#         st.write(metrics["engagement_analysis"])

#         st.subheader("Audience Quality")
#         st.write(metrics["audience_quality"])

#         st.subheader("Content Strategy")
#         st.write(metrics["content_strategy"])

#         st.subheader("Risk Assessment")
#         st.write(metrics["risk_assessment"])

#         st.subheader("Benchmark Positioning")
#         st.write(metrics["benchmark_positioning"])

#         st.subheader("Monetisation")
#         st.write(metrics["monetisation"])

#         # ---------- Video Charts ----------
#         st.subheader("Recent Video Metrics")

#         video_df = pd.DataFrame(metrics["video_data"])
#         video_df["title"] = [f"Video {i+1}" for i in range(len(video_df))]  # Optional placeholder titles

#         # Views per video
#         view_chart = alt.Chart(video_df).mark_bar().encode(
#             x=alt.X("title", sort=None, title="Videos"),
#             y=alt.Y("views", title="Views"),
#             tooltip=["title", "views", "likes", "comments", "view_to_sub_ratio"]
#         ).properties(height=300)
#         st.altair_chart(view_chart, use_container_width=True)

#         # Likes and comments per video (grouped bar)
#         lc_chart = alt.Chart(video_df.melt(id_vars=["title"], value_vars=["likes", "comments"])).mark_bar().encode(
#             x=alt.X("title", sort=None, title="Videos"),
#             y=alt.Y("value", title="Count"),
#             color="variable",
#             tooltip=["title", "variable", "value"]
#         ).properties(height=300)
#         st.altair_chart(lc_chart, use_container_width=True)

#         # Engagement rate per video
#         er_chart = alt.Chart(video_df).mark_line(point=True).encode(
#             x=alt.X("title", sort=None, title="Videos"),
#             y=alt.Y("engagement_rate", title="Engagement Rate (%)"),
#             tooltip=["title", "engagement_rate"]
#         ).properties(height=300)
#         st.altair_chart(er_chart, use_container_width=True)

#         # Top performing videos
#         st.subheader("Top Performing Videos")
#         top_videos = video_df.sort_values(by="views", ascending=False)
#         st.dataframe(top_videos[["title", "views", "likes", "comments", "engagement_rate", "view_to_sub_ratio"]])

#     else:
#         st.error("Failed to fetch metrics. Please check the channel URL/handle and try again.")
