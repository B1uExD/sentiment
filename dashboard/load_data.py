import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG

csv_file_path = r"C:\Users\rudra\Desktop\DevData\AllMyScripts\sentiment_analysis\sent_data_v2.csv"
table_name = "test_sentiment"

# Mapping: CSV column -> DB column
column_mapping = {
    "post_id": "post_id" ,
    "post": "posts",
    "post_type": "post_type",
    "sentiment_label": "sentiment_label",
    "sentiment_confidence": "sentiment_confidence",
    "category": "category",
    "severity_level": "severity_level",
    "compliance_flag": "compliance_flagged",
    "summary": "summary",
    "recommended_action": "recommended_action",
    "created_at": "created_at",
}


# Step 1: read CSV
df = pd.read_csv(csv_file_path, usecols=column_mapping.keys())

# Step 2: rename columns
df = df.rename(columns=column_mapping)

# Step 3: EXPLICIT date parsing (IMPORTANT)
df["created_at"] = pd.to_datetime(
    df["created_at"],         # forces DD-MM-YYYY
    format="%d-%m-%Y %H:%M", # fail if bad format
    errors="raise"
)

# Step 4: connect to DB
engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# Step 5: load into PostgreSQL
df.to_sql(
    table_name,
    engine,
    if_exists="append",
    index=False
)

print("Data loaded with correct date parsing!")