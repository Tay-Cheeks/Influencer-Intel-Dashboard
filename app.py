import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import isodate

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
    overview = analysis.get("overview", {})
    dashboard_score = overview.get("dashboard_score", "N/A")
    performance_label = overview.get("performance_label", "Unavailable")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Subscribers", f"{channel['subscribers']:,}")
    col2.metric("Average Views (8 videos)", f"{report.get('mean_views',0):,}")
    col3.metric("Median Views", f"{report.get('median_views',0):,}")
    col4.metric("Dashboard Score", dashboard_score, performance_label)

    # ---------------- DATAFRAME ----------------
    df = pd.DataFrame(videos)
    required_cols = {"title", "publishedAt", "views", "likes", "comments", "duration"}
    if not required_cols.issubset(df.columns):
        st.error("Video data missing required fields.")
        st.stop()

    df["published_date"] = pd.to_datetime(df["publishedAt"])
    df["label"] = df["title"] + " (" + df["published_date"].dt.strftime("%Y-%m-%d") + ")"
    df["engagement_percent"] = ((df["likes"] + df["comments"]) / df["views"]) * 100

    # ---------------- VIEWS BAR CHART ----------------
    st.subheader("Views per Recent Video")
    views_chart = (
        alt.Chart(df)
        .mark_bar(color="#1f77b4")
        .encode(
            x=alt.X("label:N", sort="-y", title="Video"),
            y=alt.Y("views:Q", title="Views"),
            tooltip=[
                alt.Tooltip("title:N", title="Title"),
                alt.Tooltip("published_date:T", title="Published"),
                alt.Tooltip("views:Q", title="Views"),
                alt.Tooltip("likes:Q", title="Likes"),
                alt.Tooltip("comments:Q", title="Comments")
            ]
        )
        .properties(height=350)
    )
    st.altair_chart(views_chart.interactive(), use_container_width=True)
    st.caption(
        "This chart shows views for the creator’s most recent 8 uploads. "
        "Average and median views are calculated from this same dataset."
    )
    st.divider()

    # ---------------- ENGAGEMENT BREAKDOWN ----------------
    st.subheader("Engagement per Video (%)")
    engagement_df = df.melt(
        id_vars=["label", "published_date", "title"],
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
            tooltip=[
                alt.Tooltip("title:N", title="Title"),
                alt.Tooltip("published_date:T", title="Published"),
                alt.Tooltip("Type:N", title="Type"),
                alt.Tooltip("Count:Q", title="Count")
            ]
        )
        .properties(height=350)
    )
    st.altair_chart(engagement_chart.interactive(), use_container_width=True)

    # Comments vs Likes explanation
    c2l_ratio = (report.get("comment_rate_percent", 0) / max(report.get("like_rate_percent", 1), 1))
    if c2l_ratio > 0.1:
        ratio_desc = "High comment-to-like ratio → audience is highly engaged in discussions."
    elif c2l_ratio < 0.02:
        ratio_desc = "Very low comment-to-like ratio → mostly passive engagement."
    else:
        ratio_desc = "Moderate comment-to-like ratio → normal engagement patterns."
    st.caption(f"Likes and comments per video help assess engagement quality. {ratio_desc}")
    st.divider()

    # ---------------- SHORTS VS LONG FORM ----------------
    st.subheader("Content Format Mix")
    sl_df = pd.DataFrame({
        "Format": ["Short-form (<7 min)", "Long-form (≥7 min)"],
        "Count": [
            sum(1 for v in videos if isodate.parse_duration(v["duration"]).total_seconds() < 420),
            sum(1 for v in videos if isodate.parse_duration(v["duration"]).total_seconds() >= 420)
        ]
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
    st.caption("A heavy short-form skew may inflate views but reduce depth and conversion.")
    st.divider()

    # ---------------- PERFORMANCE ANALYSIS ----------------
    st.subheader("Performance Analysis")
    dist = analysis.get("distribution_analysis", {})
    eng = analysis.get("engagement_analysis", {})
    aud = analysis.get("audience_quality", {})
    risk = analysis.get("risk_assessment", {})

    st.markdown(
        f"""
        **View Distribution:** {dist.get('distribution_type','N/A')}  
        {dist.get('explanation','')}
        """
    )
    st.markdown(
        f"""
        **Engagement Rate:** {eng.get('engagement_rate_percent',0)}%  
        Reflects how actively viewers interact relative to total views.  
        """
    )
    st.markdown(
        f"""
        **Audience Loyalty:** {aud.get('loyalty_percent',0)}%  
        Indicates how much of the subscriber base watches new uploads.
        """
    )
    st.markdown(
        f"""
        **Risk Level:** {risk.get('risk_level','N/A')}  
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
    st.caption("Engagement-adjusted CPM discounts inflated reach and rewards genuine interaction.")
    st.divider()

    # ---------------- AI SUMMARY ----------------
    with st.expander("AI Performance Summary"):
        ai = metrics.get_ai_analysis()
        st.write(ai.get("summary", "AI analysis unavailable."))

    # ---------------- EXPORT REPORT ----------------
    st.subheader("Export Dashboard Report")
    export_df = df.copy()
    export_df["engagement_percent"] = df["engagement_percent"]
    if st.button("Download CSV Report"):
        export_df.to_csv("youtube_dashboard_report.csv", index=False)
        st.success("CSV report saved as youtube_dashboard_report.csv")

else:
    st.info("Enter a YouTube channel and campaign details to begin.")




# import streamlit as st
# import pandas as pd
# import altair as alt
# from datetime import datetime

# from src.youtube.client import get_channel_stats, get_recent_videos
# from src.metrics.metrics import InfluencerMetrics
# from src.analysis.analyser import build_analysis

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

#     creator_url = st.text_input(
#         "YouTube Channel URL or Handle",
#         placeholder="https://youtube.com/@creator"
#     )

#     st.divider()
#     st.header("Campaign Inputs")

#     client_cost = st.number_input(
#         "Client Cost",
#         min_value=0.0,
#         step=100.0
#     )

#     agency_margin = st.slider(
#         "Agency Margin (%)",
#         min_value=0,
#         max_value=50,
#         value=20
#     )

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
#     analysis = build_analysis(metrics)

#     talent_cost = metrics.calculate_talent_cost(client_cost, agency_margin)

#     # ---------------- TOP SUMMARY ----------------
#     st.subheader(channel["channel_name"])

#     overview = analysis.get("overview", {})

#     dashboard_score = overview.get("dashboard_score", "N/A")
#     performance_label = overview.get("performance_label", "Unavailable")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Subscribers", f"{channel['subscribers']:,}")
#     col2.metric("Average Views (8 videos)", f"{report['mean_views']:,}")
#     col3.metric("Median Views", f"{report['median_views']:,}")
#     col4.metric(
#         "Dashboard Score",
#         dashboard_score,
#         performance_label
#     )


#     # ---------------- DATAFRAME ----------------
#     df = pd.DataFrame(videos)

#     # Defensive guards
#     required_cols = {"title", "publishedAt", "views", "likes", "comments", "duration"}
#     if not required_cols.issubset(df.columns):
#         st.error("Video data missing required fields.")
#         st.stop()

#     df["published_date"] = pd.to_datetime(df["publishedAt"])
#     df["label"] = df["title"] + " (" + df["published_date"].dt.strftime("%Y-%m-%d") + ")"

#     # ---------------- VIEWS BAR CHART (ALTAIR) ----------------
#     st.subheader("Views per Recent Video")

#     views_chart = (
#         alt.Chart(df)
#         .mark_bar()
#         .encode(
#             x=alt.X("label:N", sort="-y", title="Video"),
#             y=alt.Y("views:Q", title="Views"),
#             tooltip=["title", "views"]
#         )
#         .properties(height=350)
#     )

#     st.altair_chart(views_chart, use_container_width=True)

#     st.caption(
#         "This chart shows views for the creator’s most recent 8 uploads. "
#         "Average and median views are calculated from this same dataset."
#     )

#     st.divider()

#     # ---------------- ENGAGEMENT CHART ----------------
#     st.subheader("Engagement Breakdown")

#     engagement_df = df.melt(
#         id_vars=["label"],
#         value_vars=["likes", "comments"],
#         var_name="Type",
#         value_name="Count"
#     )

#     engagement_chart = (
#         alt.Chart(engagement_df)
#         .mark_bar()
#         .encode(
#             x=alt.X("label:N", title="Video"),
#             y=alt.Y("Count:Q"),
#             color="Type:N",
#             tooltip=["Type", "Count"]
#         )
#         .properties(height=350)
#     )

#     st.altair_chart(engagement_chart, use_container_width=True)

#     st.caption(
#         "Likes and comments per video help assess engagement quality, not just reach."
#     )

#     st.divider()

#     # ---------------- SHORTS VS LONG FORM ----------------
#     st.subheader("Content Format Mix")

#     sl = report["short_long_split"]
#     sl_df = pd.DataFrame({
#         "Format": ["Short-form", "Long-form"],
#         "Count": [sl["short_form"], sl["long_form"]]
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

#     st.caption(
#         "A heavy short-form skew may inflate views but reduce depth and conversion."
#     )

#     st.divider()

#     # ---------------- ANALYSIS SECTION ----------------
#     st.subheader("Performance Analysis")

#     dist = analysis["distribution_analysis"]
#     st.markdown(
#         f"""
#         **View Distribution:** {dist['distribution_type']}  
#         {dist['explanation']}
#         """
#     )

#     eng = analysis["engagement_analysis"]
#     st.markdown(
#         f"""
#         **Engagement Rate:** {eng['engagement_rate_percent']}%  
#         This reflects how actively viewers interact relative to total views.
#         """
#     )

#     aud = analysis["audience_quality"]
#     st.markdown(
#         f"""
#         **Audience Loyalty:** {aud['loyalty_percent']}%  
#         Indicates how much of the subscriber base watches new uploads.
#         """
#     )

#     risk = analysis["risk_assessment"]
#     st.markdown(
#         f"""
#         **Risk Level:** {risk['risk_level']}  
#         Based on volatility and reliance on viral spikes.
#         """
#     )

#     st.divider()

#     # ---------------- MONETISATION ----------------
#     st.subheader("Monetisation Metrics")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Client Cost", f"{client_cost:,.2f}")
#     col2.metric("Talent Cost", f"{talent_cost:,.2f}")
#     col3.metric("CPM", metrics.calculate_CPM(client_cost))
#     col4.metric("Engagement-Adjusted CPM", metrics.calculate_engagement_adjusted_CPM(client_cost))

#     st.caption(
#         "Engagement-adjusted CPM discounts inflated reach and rewards genuine interaction."
#     )

#     st.divider()

#     # ---------------- AI SUMMARY ----------------
#     with st.expander("AI Performance Summary"):
#         ai = metrics.get_ai_analysis()
#         st.write(ai.get("summary", "AI analysis unavailable."))

# else:
#     st.info("Enter a YouTube channel and campaign details to begin.")




