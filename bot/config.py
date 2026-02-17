import os
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("LEDGER_DB_PATH", str(BASE_DIR / "ledger.db"))
TIMEZONE_NAME = os.getenv("BOT_TIMEZONE", "Asia/Kolkata")


def get_timezone() -> ZoneInfo:
    try:
        return ZoneInfo(TIMEZONE_NAME)
    except Exception:
        return ZoneInfo("UTC")