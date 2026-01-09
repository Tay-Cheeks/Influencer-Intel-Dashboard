import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


from src.metrics.metrics import InfluencerMetrics
from src.analysis.analyser import build_analysis

# ---------------------------
# Streamlit config
# ---------------------------
st.set_page_config(
    page_title="Creator Performance Dashboard",
    layout="wide"
)

st.title("🎯 Creator Performance & Monetisation Dashboard")
st.caption("Data-driven influencer analysis for brand & talent decisions")

# ---------------------------
# Sidebar – Inputs for Emma
# ---------------------------
st.sidebar.header("🔗 Creator Input")

creator_url = st.sidebar.text_input(
    "YouTube Channel or Video URL",
    placeholder="https://www.youtube.com/@creator"
)

talent_cost = st.sidebar.number_input(
    "Talent Cost (ZAR)",
    min_value=0.0,
    value=400.0,
    step=50.0
)

region = st.sidebar.selectbox(
    "Primary Audience Region",
    ["South Africa", "Global", "US", "EU"]
)

run_analysis = st.sidebar.button("Run Analysis")

# ---------------------------
# Cached data fetch (daily)
# ---------------------------
@st.cache_data(ttl=86400)  # 24 hours
def get_metrics(url, talent_cost, region):
    """
    Fetch creator data + compute metrics.
    TTL ensures daily refresh.
    """

    # TODO: replace this stub with real YouTube API data
    video_data = [
        {"views": 2200, "likes": 210, "comments": 30, "days_since_posted": 2},
        {"views": 1800, "likes": 160, "comments": 18, "days_since_posted": 6},
        {"views": 2000, "likes": 180, "comments": 20, "days_since_posted": 10},
    ]

    metrics = InfluencerMetrics(
        channel_name=url,
        subscribers=12000,
        video_data=video_data,
        region=region,
        talent_cost=talent_cost
    )

    return metrics


# ---------------------------
# Run analysis
# ---------------------------
if run_analysis and creator_url:

    metrics = get_metrics(creator_url, talent_cost, region)
    analysis = build_analysis(metrics)

    report = metrics.get_performance_report()
    monetisation = metrics.get_monetisation_metrics()

    # ---------------------------
    # KPI Row
    # ---------------------------
    st.subheader("📊 Key Performance Indicators")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Mean Views", report["mean_views"])
    kpi2.metric("Median Views", report["median_views"])
    kpi3.metric("Engagement Rate", f'{report["engagement_rate_percent"]}%')
    kpi4.metric("Dashboard Score", f'{analysis["dashboard_score"]:.1f}')

    # ---------------------------
    # Mean vs Median Analysis
    # ---------------------------
    st.subheader("📈 View Distribution Health")

    view_df = pd.DataFrame({
        "Metric": ["Mean Views", "Median Views"],
        "Views": [report["mean_views"], report["median_views"]]
    })

    bar_chart = alt.Chart(view_df).mark_bar().encode(
        x="Metric",
        y="Views",
        color="Metric"
    )

    st.altair_chart(bar_chart, use_container_width=True)

    if report["mean_views"] < report["median_views"]:
        st.info(
            "Median views are higher than mean views. "
            "This indicates **stable performance without heavy spikes**."
        )
    else:
        st.warning(
            "Mean views exceed median views. "
            "Performance may be driven by a few viral videos."
        )

    # ---------------------------
    # Engagement Breakdown
    # ---------------------------
    st.subheader("💬 Engagement Composition")

    engagement_df = pd.DataFrame({
        "Type": ["Likes", "Comments"],
        "Rate (%)": [
            report["like_rate_percent"],
            report["comment_rate_percent"]
        ]
    })

    pie_chart = alt.Chart(engagement_df).mark_arc().encode(
        theta="Rate (%)",
        color="Type"
    )

    st.altair_chart(pie_chart, use_container_width=True)

    # ---------------------------
    # Consistency & Risk
    # ---------------------------
    st.subheader("⚠️ Risk & Consistency Signals")

    st.write(f"**Risk Level:** {report['risk_level']}")
    st.write("**Anti-Fraud Checks:**")

    for signal, value in report["anti_fraud_signals"].items():
        if value:
            st.error(f"⚠️ {signal.replace('_', ' ').title()}")
        else:
            st.success(f"✓ {signal.replace('_', ' ').title()}")

    # ---------------------------
    # Monetisation Metrics
    # ---------------------------
    st.subheader("💰 Monetisation Snapshot")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("CPM", f"R{monetisation['cpm']}")
    m2.metric("CPE", f"R{monetisation['cpe']}")
    m3.metric("CPV", f"R{monetisation['cpv']}")
    m4.metric("Adj. CPM", f"R{monetisation['engagement_adjusted_cpm']}")

    # ---------------------------
    # Final Recommendation
    # ---------------------------
    st.subheader("🧠 Analyst Summary")

    st.markdown(f"""
    **Overall Rating:** {analysis["interpretation"]}

    **Why this matters for Emma:**
    - Consistency score suggests **predictable delivery**
    - Engagement sits **above benchmark**
    - Cost efficiency is **acceptable for branded campaigns**
    """)

    st.caption(f"Last refreshed: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
