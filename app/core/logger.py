import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = "logs/"

os.makedirs(LOG_DIR, exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s:%(lineno)d | %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
    delay=False,
)
file_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler],
    format="%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s:%(lineno)d | %(message)s",
)

logger = logging.getLogger(__name__)
