from loguru import logger
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "dashboard.log")

# create logs folder if not exists
os.makedirs(LOG_DIR, exist_ok=True)

# remove default logger (optional but clean)
logger.remove()

# console logging
logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO"
)

# file logging (production-ready)
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    enqueue=True
)