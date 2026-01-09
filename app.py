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
else:
    alt.themes.enable("light")

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

    # ---------------- DASHBOARD SCORE EXPLANATION ------------
    with st.expander("What is the Dashboard Score?"):
        st.markdown(
            """
            **Dashboard Score (0–100)** is a composite performance index designed to give a 
            quick, decision-ready view of a creator’s overall quality.

            It combines:
            • Engagement rate vs industry benchmarks  
            • Audience loyalty (views-to-subscriber ratio)  
            • Engagement consistency (volatility control)  
            • Content risk profile (viral vs stable performance)

            **Higher scores indicate creators who are more reliable, brand-safe, and commercially scalable.**
            """
        )


    # ---------------- DATA ----------------
    df = pd.DataFrame(videos)
    df["published_date"] = pd.to_datetime(df["publishedAt"])
    df["engagement"] = df["likes"] + df["comments"]

    # ---------------- AVRG vs MEDIAN VIEWS & VOLATILITY ----------------
    st.subheader("View Performance Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Views",
        f"{report['mean_views']:,}",
        help="Average views across recent uploads. Can be inflated by viral videos."
    )

    col2.metric(
        "Median Views",
        f"{report['median_views']:,}",
        help="Typical views per video. More reliable indicator of baseline performance."
    )

    col3.metric(
        "Volatility & Risk",
        report["risk_level"],
        help=f"Volatility Ratio: {report['volatility_ratio']} (Higher = less predictable)"
    )

    st.caption(
        """
        A large gap between average and median views indicates volatility. 
        Brands prefer creators with strong median performance and low volatility.
        """
    )


    # ---------------- PERFORMANCE CHART ----------------
    st.subheader("Performance & Velocity")
    st.caption(
        """
        This section evaluates how consistently the creator performs over time 
        and whether recent content is gaining momentum. 
        It helps identify if performance is stable, declining, or driven by short-term spikes.
        """
    )

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

    # ---------------- VIDEO VIEWS CHART ---------------------
    st.subheader("Views per Recent Video")

    views_chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("title:N", sort="-y", title="Video"),
            y=alt.Y("views:Q", title="Views"),
            tooltip=[
                alt.Tooltip("title:N", title="Video"),
                alt.Tooltip("views:Q", title="Views"),
                alt.Tooltip("published_date:T", title="Published")
            ]
        )
        .properties(height=350)
        .interactive()
    )

    st.altair_chart(views_chart, use_container_width=True)

    st.caption("Hover over bars to see detailed performance per video.")


    # ---------------- LIKES vs COMMENTS CHART ---------------
    st.subheader("Engagement Breakdown")

    eng_df = df.melt(
        id_vars=["title", "published_date"],
        value_vars=["likes", "comments"],
        var_name="Engagement Type",
        value_name="Count"
    )

    eng_chart = (
        alt.Chart(eng_df)
        .mark_bar()
        .encode(
            x=alt.X("title:N", title="Video"),
            y=alt.Y("Count:Q", title="Engagement"),
            color=alt.Color("Engagement Type:N"),
            tooltip=[
                "Engagement Type",
                "Count",
                alt.Tooltip("published_date:T", title="Published")
            ]
        )
        .properties(height=350)
        .interactive()
    )

    st.altair_chart(eng_chart, use_container_width=True)

    st.caption("Balanced comment-to-like ratios typically indicate healthier engagement.")


    # ---------------- SHORT vs LONG ANALYSIS ----------------
    st.subheader("Short vs Long Content Mix")

    sl = report["short_long_split"]

    sl_df = pd.DataFrame({
        "Format": ["Short-form (<7 min)", "Long-form (≥7 min)"],
        "Count": [sl["short_count"], sl["long_count"]]
    })

    pie_chart = (
        alt.Chart(sl_df)
        .mark_arc(innerRadius=40)
        .encode(
            theta=alt.Theta("Count:Q"),
            color=alt.Color("Format:N", legend=alt.Legend(title="Content Type")),
            tooltip=["Format", "Count"]
        )
        .properties(height=300)
    )

    st.altair_chart(pie_chart, use_container_width=True)

    st.caption(
        f"""
        Short-form accounts for **{sl['short_percent']}%** of recent content.
        Short-form typically boosts reach, while long-form drives depth and retention.
        """
    )

    # st.subheader("Short vs Long Content Mix")

    # sl = report["short_long_split"]
    # sl_df = pd.DataFrame({
    #     "Format": ["Short-form", "Long-form"],
    #     "Count": [sl["short_count"], sl["long_count"]],
    #     "Avg Views": [sl["short_avg_views"], sl["long_avg_views"]],
    # })

    # st.altair_chart(
    #     alt.Chart(sl_df)
    #     .mark_bar()
    #     .encode(
    #         x="Format:N",
    #         y="Count:Q",
    #         color="Format:N",
    #         tooltip=["Count", "Avg Views"]
    #     ),
    #     use_container_width=True
    # )

    # conclusion = (
    #     "Short-form dominates reach but long-form drives depth."
    #     if sl["short_count"] > sl["long_count"]
    #     else "Long-form content drives sustained audience value."
    # )

    # st.caption(conclusion)

    # ---------------- MONETISATION ----------------
    st.subheader("Monetisation Metrics")

    st.markdown("### CPM — Cost Per 1,000 Views")
    st.write(
        f"""
        **Result:** {metrics.calculate_CPM(client_cost)}  
        Measures cost efficiency of reach. Lower CPM = better value for brands.
        """
    )

    st.markdown("### CPV — Cost Per View")
    st.write(
        f"""
        **Result:** {metrics.calculate_CPV(client_cost)}  
        Shows how much each individual view costs. Useful for awareness campaigns.
        """
    )

    st.markdown("### CPE — Cost Per Engagement")
    st.write(
        f"""
        **Result:** {metrics.calculate_CPE(client_cost)}  
        Indicates engagement efficiency. Lower CPE suggests stronger audience interaction.
        """
    )

    st.markdown("### Engagement-Adjusted CPM")
    st.write(
        f"""
        **Result:** {metrics.calculate_engagement_adjusted_CPM(client_cost)}  
        Adjusts CPM based on engagement quality — rewards creators with active audiences.
        """
    )

    st.markdown("### Talent Cost (After Agency Margin)")
    st.write(
        f"""
        **Result:** {metrics.calculate_talent_cost(client_cost, agency_margin):,.2f}  
        Net payout to creator after agency margin.
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





