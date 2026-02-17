import logging
from datetime import datetime
from telegram import Update, constants, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import BOT_TOKEN, DATABASE_URL, get_timezone
from database import Database
from parser import parse_transaction
from reports import build_report
from scheduler import setup_scheduler


async def set_commands(application: Application):
    await application.bot.set_my_commands([
        BotCommand("start", "Initialize the bot"),
        BotCommand("daily", "Today’s detailed report"),
        BotCommand("weekly", "This week’s detailed report"),
        BotCommand("monthly", "This month’s detailed report"),
        BotCommand("help", "View syntax and manual"),
    ])


logging.basicConfig(level=logging.INFO)


def _now(tz):
    return datetime.now(tz)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cash Flow Ledger initialized.\nUse /help for instructions."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use:\n+100 Salary\n-50 Dinner\n\n"
        "/daily\n/weekly\n/monthly",
    )


async def add_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    parsed = parse_transaction(update.message.text)
    if not parsed:
        await update.message.reply_text(
            "Invalid format. Use '+100 salary' or '-250 groceries'."
        )
        return

    db: Database = context.application.bot_data["database"]

    db.add_transaction(
        update.effective_user.id,
        parsed["amount"],
        parsed["type"],
        parsed["details"],
    )


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE, period: str):
    if not update.effective_user or not update.message:
        return

    db: Database = context.application.bot_data["database"]
    tz = context.application.bot_data["timezone"]

    report = build_report(db, update.effective_user.id, period, _now(tz))
    await update.message.reply_text(report)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set")

    db = Database(DATABASE_URL)
    tz = get_timezone()

    app = Application.builder().token(BOT_TOKEN).build()
    app.bot_data["database"] = db
    app.bot_data["timezone"] = tz

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("daily", lambda u, c: report_command(u, c, "daily")))
    app.add_handler(CommandHandler("weekly", lambda u, c: report_command(u, c, "weekly")))
    app.add_handler(CommandHandler("monthly", lambda u, c: report_command(u, c, "monthly")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_transaction))

    app.post_init = set_commands
    setup_scheduler(app, db, tz)

    app.run_polling()


if __name__ == "__main__":
    main()
