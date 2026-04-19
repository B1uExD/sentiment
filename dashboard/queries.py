from config import DEFAULT_TABLE, TIME_COLUMN


def build_time_filtered_query(time_window: str):

    if time_window == "Last 24 Hours":
        interval = "24 hours"

    elif time_window == "Last 7 Days":
        interval = "7 days"

    elif time_window == "Last 1 Month":
        interval = "1 month"

    else:
        interval = "24 hours"

    return f"""
        SELECT *
        FROM {DEFAULT_TABLE}
        WHERE {TIME_COLUMN} >= NOW() - INTERVAL '{interval}'
        ORDER BY {TIME_COLUMN} DESC
    """