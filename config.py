import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/cash_flow_ledger",
)
TIMEZONE_NAME = os.getenv("BOT_TIMEZONE", "Asia/Kolkata")


def get_timezone() -> ZoneInfo:
    try:
        return ZoneInfo(TIMEZONE_NAME)
    except Exception:
        return ZoneInfo("UTC")
