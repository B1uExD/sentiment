import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG
from logger_config import logger


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )


def fetch_data(query: str) -> pd.DataFrame:
    logger.info(f"Executing query:\n{query}")

    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        logger.info(f"Query successful → {len(df)} rows fetched")
        return df

    except Exception as e:
        logger.error(f"Database query failed: {e}")
        raise