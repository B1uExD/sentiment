import pandas as pd
import duckdb


# -----------------------------
# DATA CLEANING LAYER
# -----------------------------
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes dataframe types for safe analytics.
    """

    if df is None or df.empty:
        return df

    # 🔥 Convert numeric columns safely
    numeric_cols = [
        "sentiment_confidence"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# -----------------------------
# PANDAS → DUCKDB SETUP
# -----------------------------
def register_duckdb(df: pd.DataFrame):
    """
    Registers dataframe into DuckDB for fast SQL analytics.
    """
    con = duckdb.connect()
    con.register("df_view", df)
    return con


# -----------------------------
# KPI CALCULATIONS (FIXED)
# -----------------------------
def get_kpis(df: pd.DataFrame):
    """
    Computes dashboard KPIs safely.
    """

    df = clean_dataframe(df)

    total_posts = len(df)

    complaints = len(df[df["post_type"] == "Complaint"]) if "post_type" in df.columns else 0

    fraud_cases = len(df[df["category"] == "Fraud/Phishing"]) if "category" in df.columns else 0

    # 🔥 SAFE MEAN CALCULATION (FIXED ERROR HERE)
    avg_confidence = (
        df["sentiment_confidence"].mean()
        if "sentiment_confidence" in df.columns
        else 0
    )

    # handle NaN safely
    avg_confidence = 0 if pd.isna(avg_confidence) else round(avg_confidence, 2)

    return {
        "total_posts": total_posts,
        "complaints": complaints,
        "fraud_cases": fraud_cases,
        "avg_confidence": avg_confidence
    }


# -----------------------------
# DUCKDB ANALYTICS QUERIES
# -----------------------------
def get_sentiment_distribution(con):
    return con.execute("""
        SELECT sentiment_label, COUNT(*) AS count
        FROM df_view
        GROUP BY sentiment_label
        ORDER BY count DESC
    """).df()


def get_category_breakdown(con):
    return con.execute("""
        SELECT category, COUNT(*) AS count
        FROM df_view
        GROUP BY category
        ORDER BY count DESC
    """).df()


def get_severity_distribution(con):
    return con.execute("""
        SELECT severity_level, COUNT(*) AS count
        FROM df_view
        GROUP BY severity_level
        ORDER BY count DESC
    """).df()


def get_compliance_issues(con):
    return con.execute("""
        SELECT compliance_flagged, COUNT(*) AS count
        FROM df_view
        GROUP BY compliance_flagged
        ORDER BY count DESC
    """).df()