import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

from src.youtube.client import get_channel_stats, get_recent_videos
from src.metrics.metrics import InfluencerMetrics
from src.analysis.analyser import get_creator_tier

# ---------------- THEME TOGGLE ----------------
theme = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme == "Dark":
    alt.themes.enable("dark")

st.set_page_config(page_title="Influencer Intel Dashboard", layout="wide")

st.title("Influencer Intel Dashboard")
st.caption("Performance • Engagement • Monetisation")

# ---------------- INPUTS ----------------
with st.sidebar:
    creator_url = st.text_input("YouTube Channel URL / Handle")
    client_cost = st.number_input("Client Cost", min_value=0.0, step=100.0)
    agency_margin = st.slider("Agency Margin (%)", 0, 50, 20)
    run = st.button("Run Analysis", type="primary")

# ---------------- RUN ----------------
if run and creator_url:
    channel = get_channel_stats(creator_url)
    videos = get_recent_videos(channel["uploads_playlist_id"], count=8)

    metrics = InfluencerMetrics(
        channel_name=channel["channel_name"],
        sub_count=channel["subscribers"],
        video_data=videos
    )

    report = metrics.get_performance_report()
    creator_tier = get_creator_tier(channel["subscribers"])

    # ---------------- SUMMARY ----------------
    st.subheader(f"{channel['channel_name']} • {creator_tier}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Subscribers", f"{channel['subscribers']:,}")
    c2.metric("Mean Views", f"{report['mean_views']:,}")
    c3.metric("Median Views", f"{report['median_views']:,}")
    c4.metric("Dashboard Score", metrics.dashboard_score, metrics.dashboard_interpretation)

    # ---------------- DATA ----------------
    df = pd.DataFrame(videos)
    df["published_date"] = pd.to_datetime(df["publishedAt"])
    df["engagement"] = df["likes"] + df["comments"]

    # ---------------- PERFORMANCE CHART ----------------
    st.subheader("Performance & Velocity")
    perf_chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x="published_date:T",
            y="views:Q",
            tooltip=["title", "views"]
        )
        .properties(height=300)
    )
    st.altair_chart(perf_chart, use_container_width=True)

    st.markdown(
        f"""
        **Risk:** {report['risk_level']}  
        **Velocity (7d):** {report['velocity_views_7d']:,} views  
        **Benchmark Velocity Contribution:** High-performing creators ≥ 25%
        """
    )

    # ---------------- SHORT vs LONG ANALYSIS ----------------
    st.subheader("Short vs Long Content Mix")

    sl = report["short_long_split"]
    sl_df = pd.DataFrame({
        "Format": ["Short-form", "Long-form"],
        "Count": [sl["short_count"], sl["long_count"]],
        "Avg Views": [sl["short_avg_views"], sl["long_avg_views"]],
    })

    st.altair_chart(
        alt.Chart(sl_df)
        .mark_bar()
        .encode(
            x="Format:N",
            y="Count:Q",
            color="Format:N",
            tooltip=["Count", "Avg Views"]
        ),
        use_container_width=True
    )

    conclusion = (
        "Short-form dominates reach but long-form drives depth."
        if sl["short_count"] > sl["long_count"]
        else "Long-form content drives sustained audience value."
    )

    st.caption(conclusion)

    # ---------------- MONETISATION ----------------
    st.subheader("Monetisation Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CPM", metrics.calculate_CPM(client_cost))
    col2.metric("CPV", metrics.calculate_CPV(client_cost))
    col3.metric("CPE", metrics.calculate_CPE(client_cost))
    col4.metric("Engagement-Adj CPM", metrics.calculate_engagement_adjusted_CPM(client_cost))

    st.caption(
        """
        • **CPM Benchmark:** R30–R60  
        • **Low CPV:** Efficient reach  
        • **Low CPE:** High engagement quality
        """
    )

    # ---------------- CSV EXPORT ----------------
    st.subheader("Export Report")
    export_df = pd.DataFrame([{
        **report,
        "CPM": metrics.calculate_CPM(client_cost),
        "CPV": metrics.calculate_CPV(client_cost),
        "CPE": metrics.calculate_CPE(client_cost),
        "Talent Cost": metrics.calculate_talent_cost(client_cost, agency_margin),
        "Dashboard Score": metrics.dashboard_score,
    }])

    st.download_button(
        "Download CSV (Sheets-ready)",
        export_df.to_csv(index=False),
        file_name=f"{channel['channel_name']}_report.csv",
        mime="text/csv"
    )

else:
    st.info("Enter a channel and campaign details to begin.")




# import streamlit as st
# import pandas as pd
# import altair as alt
# from datetime import datetime
# import json

# from src.youtube.client import get_channel_stats, get_recent_videos
# from src.metrics.metrics import InfluencerMetrics
# from src.analysis.analyser import build_analysis, get_creator_tier

# # ---------------- STREAMLIT CONFIG ----------------
# st.set_page_config(
#     page_title="Influencer Intel Dashboard",
#     layout="wide"
# )

# st.title("Influencer Intel Dashboard")
# st.caption("Data-driven influencer performance, engagement & monetisation analysis")

# # ---------------- SIDEBAR INPUTS ----------------
# with st.sidebar:
#     st.header("Channel Input")
#     creator_url = st.text_input("YouTube Channel URL or Handle", placeholder="https://youtube.com/@creator")

#     st.divider()
#     st.header("Campaign Inputs")
#     client_cost = st.number_input("Client Cost", min_value=0.0, step=100.0)
#     agency_margin = st.slider("Agency Margin (%)", min_value=0, max_value=50, value=20)
#     run_btn = st.button("Run Analysis", type="primary")

# # ---------------- MAIN LOGIC ----------------
# if run_btn and creator_url:
#     with st.spinner("Fetching YouTube data..."):
#         channel = get_channel_stats(creator_url)
#         if not channel:
#             st.error("Could not fetch channel data.")
#             st.stop()

#         videos = get_recent_videos(channel["uploads_playlist_id"], count=8)
#         if not videos:
#             st.error("No recent videos found.")
#             st.stop()

#     metrics = InfluencerMetrics(
#         channel_name=channel["channel_name"],
#         sub_count=channel["subscribers"],
#         video_data=videos,
#         region=channel["region"]
#     )

#     report = metrics.get_performance_report()
#     talent_cost = metrics.calculate_talent_cost(client_cost, agency_margin)

#     # ---------------- ANALYSIS ----------------
#     analysis = build_analysis(metrics)
#     creator_tier = get_creator_tier(metrics.sub_count)

#     # ---------------- TOP SUMMARY ----------------
#     st.subheader(f"{channel['channel_name']} ({creator_tier})")
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Subscribers", f"{channel['subscribers']:,}")
#     col2.metric("Average Views (8 videos)", f"{report['mean_views']:,}")
#     col3.metric("Median Views", f"{report['median_views']:,}")
#     col4.metric("Dashboard Score", metrics.dashboard_score, metrics.dashboard_interpretation)

#     # ---------------- DATAFRAME ----------------
#     df = pd.DataFrame(videos)
#     df["published_date"] = pd.to_datetime(df["publishedAt"])
#     df["label"] = df["title"] + " (" + df["published_date"].dt.strftime("%Y-%m-%d") + ")"

#     # ---------------- VIEWS BAR CHART ----------------
#     st.subheader("Views per Recent Video")
#     views_chart = (
#         alt.Chart(df)
#         .mark_bar()
#         .encode(
#             x=alt.X("label:N", sort="-y", title="Video"),
#             y=alt.Y("views:Q", title="Views"),
#             tooltip=["title", "views", alt.Tooltip("published_date:T", title="Date")]
#         )
#         .properties(height=350)
#     )
#     st.altair_chart(views_chart, use_container_width=True)
#     st.caption("This chart shows views for the creator’s most recent 8 uploads.")

#     # ---------------- ENGAGEMENT CHART ----------------
#     st.subheader("Engagement Breakdown")
#     engagement_df = df.melt(
#         id_vars=["label", "published_date"],
#         value_vars=["likes", "comments"],
#         var_name="Type",
#         value_name="Count"
#     )

#     engagement_chart = (
#         alt.Chart(engagement_df)
#         .mark_bar()
#         .encode(
#             x=alt.X("label:N", title="Video"),
#             y=alt.Y("Count:Q", title="Engagement"),
#             color="Type:N",
#             order=alt.Order('Type', sort='ascending'),  # comments below likes
#             tooltip=["label", "Type", "Count", alt.Tooltip("published_date:T", title="Date")]
#         )
#         .properties(height=350)
#     )
#     st.altair_chart(engagement_chart, use_container_width=True)
#     st.caption("Likes and comments per video. Moderate comment-to-like ratio → normal engagement.")

#     # ---------------- SHORTS VS LONG FORM ----------------
#     st.subheader("Content Format Mix")
#     sl_df = pd.DataFrame({
#         "Format": ["Short-form (<7 min)", "Long-form (≥7 min)"],
#         "Count": [report["short_long_split"]["short_form"], report["short_long_split"]["long_form"]]
#     })
#     format_chart = (
#         alt.Chart(sl_df)
#         .mark_arc()
#         .encode(
#             theta="Count:Q",
#             color="Format:N",
#             tooltip=["Format", "Count"]
#         )
#         .properties(height=300)
#     )
#     st.altair_chart(format_chart, use_container_width=True)
#     st.caption("Short-form skew may inflate views but reduce depth.")

#     # ---------------- PERFORMANCE ANALYSIS ----------------
#     st.subheader("Performance Analysis")
#     dist = analysis["views_distribution"]
#     eng = analysis["engagement"]
#     aud = analysis["audience_loyalty"]
#     risk = analysis["risk"]

#     st.markdown(f"**View Distribution:** {dist['type']}  \n{dist['explanation']}")
#     st.markdown(f"**Engagement Rate:** {eng['rate']}%  \nBenchmark: {eng['benchmark_position']}")
#     st.markdown(f"**Audience Loyalty:** {aud['loyalty_percent']}%  \nBenchmark: {aud['benchmark_position']}")
#     st.markdown(f"**Risk Level:** {risk['risk_level']}")

#     # ---------------- MONETISATION ----------------
#     st.subheader("Monetisation Metrics")
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Client Cost", f"{client_cost:,.2f}")
#     col2.metric("Talent Cost", f"{talent_cost:,.2f}")
#     col3.metric("CPM", metrics.calculate_CPM(client_cost))
#     col4.metric("Engagement-Adjusted CPM", metrics.calculate_engagement_adjusted_CPM(client_cost))

#     # ---------------- AI SUMMARY ----------------
#     with st.expander("AI Performance Summary"):
#         ai = metrics.get_ai_analysis()
#         st.write(ai.get("summary", "AI analysis unavailable."))

#     # ---------------- EXPORT REPORT ----------------
#     st.subheader("Export Dashboard Report")
#     report_export = {
#         "channel": channel,
#         "creator_tier": creator_tier,
#         "metrics": report,
#         "analysis": analysis,
#         "monetisation": {
#             "client_cost": client_cost,
#             "talent_cost": talent_cost,
#             "CPM": metrics.calculate_CPM(client_cost),
#             "engagement_adjusted_CPM": metrics.calculate_engagement_adjusted_CPM(client_cost)
#         },
#         "AI_summary": ai
#     }
#     st.download_button(
#         label="Download Report as JSON",
#         data=json.dumps(report_export, indent=2),
#         file_name=f"{channel['channel_name']}_dashboard_report.json",
#         mime="application/json"
#     )

# else:
#     st.info("Enter a YouTube channel and campaign details to begin.")





