import streamlit as st
import pandas as pd
import altair as alt
from src.metrics.metrics import InfluencerMetrics
from src.analysis.analyzer import build_analysis
from src.youtube.client import get_channel_stats, get_recent_videos

# ---------- App Config ----------
st.set_page_config(page_title="Influencer Intel Dashboard", layout="wide")
st.title("Influencer Intel Dashboard")
st.write("Analyze YouTube influencer performance and monetisation metrics.")

# ---------- Input ----------
creator_input = st.text_input("YouTube Channel URL / Handle / ID")
client_cost = st.number_input("Client Cost (in your currency)", min_value=0.0, step=1.0)
agency_margin = st.number_input("Agency Margin %", min_value=0.0, max_value=100.0, step=1.0)

# ---------- Fetch & Process Data ----------
@st.cache_data(ttl=3600)
def get_metrics(creator_input, client_cost, agency_margin):
    # Step 1: Fetch channel stats
    channel_stats = get_channel_stats(creator_input)
    if not channel_stats:
        return None

    sub_count = channel_stats["subscribers"]
    playlist_id = channel_stats["uploads_playlist_id"]
    region = channel_stats["region"]

    # Step 2: Fetch recent videos
    video_data = get_recent_videos(playlist_id, count=8)
    if not video_data:
        return None

    # Step 3: Create InfluencerMetrics instance
    metrics = InfluencerMetrics(
        channel_name=channel_stats["channel_name"],
        sub_count=sub_count,
        video_data=video_data,
        region=region
    )

    # Step 4: Calculate talent cost
    talent_cost = metrics.calculate_talent_cost(client_cost, agency_margin)

    # Step 5: Build analysis
    analysis_report = build_analysis(metrics)

    # Add monetisation info
    analysis_report["monetisation"] = {
        "client_cost": client_cost,
        "agency_margin_percent": agency_margin,
        "talent_cost": talent_cost,
        "avg_views_recent": round(sum(v["views"] for v in video_data)/len(video_data), 2),
        "median_views_recent": round(pd.Series([v["views"] for v in video_data]).median(), 2)
    }

    # Add video data for charts
    # Calculate view-to-sub ratio for each video
    for v in video_data:
        v["view_to_sub_ratio"] = round((v["views"] / sub_count * 100) if sub_count else 0, 2)
        v["engagement_rate"] = round(((v["likes"] + v["comments"]) / v["views"] * 100) if v["views"] else 0, 2)

    analysis_report["video_data"] = video_data

    return analysis_report

# ---------- Main ----------
if creator_input:
    with st.spinner("Fetching metrics..."):
        metrics = get_metrics(creator_input, client_cost, agency_margin)

    if metrics:
        st.subheader("Channel Overview")
        st.write(metrics["overview"])

        st.subheader("Distribution Analysis")
        st.write(metrics["distribution_analysis"])

        st.subheader("Engagement Analysis")
        st.write(metrics["engagement_analysis"])

        st.subheader("Audience Quality")
        st.write(metrics["audience_quality"])

        st.subheader("Content Strategy")
        st.write(metrics["content_strategy"])

        st.subheader("Risk Assessment")
        st.write(metrics["risk_assessment"])

        st.subheader("Benchmark Positioning")
        st.write(metrics["benchmark_positioning"])

        st.subheader("Monetisation")
        st.write(metrics["monetisation"])

        # ---------- Video Charts ----------
        st.subheader("Recent Video Metrics")

        video_df = pd.DataFrame(metrics["video_data"])
        video_df["title"] = [f"Video {i+1}" for i in range(len(video_df))]  # Optional placeholder titles

        # Views per video
        view_chart = alt.Chart(video_df).mark_bar().encode(
            x=alt.X("title", sort=None, title="Videos"),
            y=alt.Y("views", title="Views"),
            tooltip=["title", "views", "likes", "comments", "view_to_sub_ratio"]
        ).properties(height=300)
        st.altair_chart(view_chart, use_container_width=True)

        # Likes and comments per video (grouped bar)
        lc_chart = alt.Chart(video_df.melt(id_vars=["title"], value_vars=["likes", "comments"])).mark_bar().encode(
            x=alt.X("title", sort=None, title="Videos"),
            y=alt.Y("value", title="Count"),
            color="variable",
            tooltip=["title", "variable", "value"]
        ).properties(height=300)
        st.altair_chart(lc_chart, use_container_width=True)

        # Engagement rate per video
        er_chart = alt.Chart(video_df).mark_line(point=True).encode(
            x=alt.X("title", sort=None, title="Videos"),
            y=alt.Y("engagement_rate", title="Engagement Rate (%)"),
            tooltip=["title", "engagement_rate"]
        ).properties(height=300)
        st.altair_chart(er_chart, use_container_width=True)

        # Top performing videos
        st.subheader("Top Performing Videos")
        top_videos = video_df.sort_values(by="views", ascending=False)
        st.dataframe(top_videos[["title", "views", "likes", "comments", "engagement_rate", "view_to_sub_ratio"]])

    else:
        st.error("Failed to fetch metrics. Please check the channel URL/handle and try again.")
