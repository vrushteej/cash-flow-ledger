"""Configuration file for the Telegram Finance Bot."""
import os

# Telegram Bot Token - Get it from BotFather
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Database configuration
DATABASE_PATH = 'finance_bot.db'

# Timezone for scheduling
TIMEZONE = 'UTC'

# Report times (24-hour format)
DAILY_REPORT_TIME = '23:59'
WEEKLY_REPORT_TIME = '23:59'
MONTHLY_REPORT_TIME = '23:59'
