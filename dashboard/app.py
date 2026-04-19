import streamlit as st
from streamlit_autorefresh import st_autorefresh

from database import fetch_data
from queries import build_time_filtered_query
from transformations import (
    register_duckdb,
    get_sentiment_distribution,
    get_category_breakdown,
    get_severity_distribution,
    get_compliance_issues,
    get_kpis
)

from logger_config import logger


# -----------------------------
# AUTO REFRESH CONFIG
# -----------------------------

def enable_auto_refresh(time_window: str):
    """
    Enable refresh only when needed (optional logic).
    """

    # Example: only auto-refresh for real-time views
    if time_window == "Last 24 Hours":
        st_autorefresh(interval=60000, key="live_refresh")  # 60 sec
        logger.info("Auto-refresh enabled (60s)")
    else:
        logger.info("Auto-refresh disabled for long-range view")


# -----------------------------
# DATA LOADER
# -----------------------------

def load_data(time_window: str):
    query = build_time_filtered_query(time_window)
    df = fetch_data(query)
    logger.info(f"Data loaded for: {time_window}")
    return df


# -----------------------------
# DASHBOARD UI
# -----------------------------

def render_dashboard(df):
    st.title("📊 Insights Dashboard")

    if df.empty:
        logger.warning("Empty dataset returned")
        st.warning("No data found")
        return

    kpis = get_kpis(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Posts", kpis["total_posts"])
    col2.metric("Complaints", kpis["complaints"])
    col3.metric("Fraud Cases", kpis["fraud_cases"])
    col4.metric("Avg Confidence", kpis["avg_confidence"])

    con = register_duckdb(df)

    st.subheader("Sentiment")
    st.bar_chart(get_sentiment_distribution(con).set_index("sentiment_label"))

    st.subheader("Category")
    st.bar_chart(get_category_breakdown(con).set_index("category"))

    st.subheader("Severity")
    st.bar_chart(get_severity_distribution(con).set_index("severity_level"))

    st.subheader("Compliance")
    st.bar_chart(get_compliance_issues(con).set_index("compliance_flagged"))

    st.subheader("Raw Data")
    st.dataframe(df)


# -----------------------------
# MAIN APP
# -----------------------------

def main():
    logger.info("Dashboard started")

    st.sidebar.title("Filters")

    time_window = st.sidebar.selectbox(
        "Time Range",
        ["Last 24 Hours", "Last 7 Days", "Last 1 Month"],
        index=0
    )

    logger.info(f"Selected time window: {time_window}")

    # 🔄 AUTO REFRESH TRIGGER
    enable_auto_refresh(time_window)

    # 📥 LOAD DATA
    df = load_data(time_window)

    # 📊 RENDER UI
    render_dashboard(df)

    logger.info("Dashboard render complete")


if __name__ == "__main__":
    main()