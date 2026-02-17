from datetime import datetime, time, timedelta

from telegram.ext import Application, ContextTypes

from database import Database
from reports import build_report
from reports import build_summary

async def _scheduled_summary_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    database: Database = context.job.data["database"]
    tz = context.job.data["tz"]
    now = datetime.now(tz)

    for user_id in database.list_user_ids():
        daily_text = build_summary(database, user_id, "daily", now)
        await context.bot.send_message(chat_id=user_id, text=daily_text)

        if now.weekday() == 6:
            weekly_text = build_report(database, user_id, "weekly", now)
            await context.bot.send_message(chat_id=user_id, text=weekly_text)

        tomorrow = now + timedelta(days=1)
        if tomorrow.month != now.month:
            monthly_text = build_report(database, user_id, "monthly", now)
            await context.bot.send_message(chat_id=user_id, text=monthly_text)


def setup_scheduler(application: Application, database: Database, tz) -> None:
    application.job_queue.run_daily(
        _scheduled_summary_job,
        time=time(hour=23, minute=59, tzinfo=tz),
        data={"database": database, "tz": tz},
        name="finance-summaries",
    )