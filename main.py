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
        BotCommand("daily", "View today’s transactions"),
        BotCommand("weekly", "View this week’s summary"),
        BotCommand("monthly", "View this month’s summary"),
        BotCommand("help", "View syntax and manual"),
    ])

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def _now(tz):
    return datetime.now(tz)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "<b>Welcome to Cash Flow Ledger.</b> 🏛️\n\n"
        "I am your financial co-pilot. I turn your messages into a "
        "professional-grade ledger, keeping your wealth in focus "
        "without the spreadsheets.\n\n"
        
        "<b>Log your flow instantly:</b>\n"
        "➕ <code>+100 Dividend</code>\n"
        "➖ <code>-50 Dinner</code>\n\n"
        
        "<b>Command your data:</b>\n"
        "📈 /daily • Today’s snapshot\n"
        "🗓️ /weekly • The week’s momentum\n"
        "📊 /monthly • Your monthly horizon\n\n"
        
        "<i>Ready to master your capital? Enter your first transaction.</i>"
    )

    await update.message.reply_text(
        text=welcome_text,
        parse_mode=constants.ParseMode.HTML
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🛠 <b>Cash Flow Ledger: Manual</b>\n\n"
        
        "<b>How to Log Data</b>\n"
        "Every entry requires a prefix, an amount, and a label.\n\n"
        "• ➕ <b>[+] Plus Prefix:</b> Registers income (Gain).\n"
        "<i>Example: +1000 Client A stores 1000 in your Gain column.</i>\n\n"
        "• ➖ <b>[-] Minus Prefix:</b> Registers an expense (Spend).\n"
        "<i>Example: -50 Fuel stores 50 in your Spend column.</i>\n\n"
        "• <b>Decimals:</b> Use a period (.) for cents (e.g., -4.50 Coffee).\n\n"
        
        "<b>Generate Reports</b>\n"
        "• /daily — Lists every transaction recorded today.\n"
        "• /weekly — Summarizes total gains and spends for the current week.\n"
        "• /monthly — Calculates total balance and net flow for the current month.\n\n"
        
        "<b>Automatic summaries</b>\n"
        "• Daily summary at 11:59 PM\n"
        "• Weekly summary every Sunday at 11:59 PM\n"
        "• Monthly summary on the last day at 11:59 PM"
    )

    await update.message.reply_text(
        text=help_text,
        parse_mode=constants.ParseMode.HTML
    )

async def add_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    if update.effective_user is None or update.message is None:
        return

    parsed = parse_transaction(update.message.text)
    if parsed is None:
        await update.message.reply_text( "Invalid format. Use '+100 salary' or '-250 groceries'." )
        return

    db: Database = context.application.bot_data["database"]
    db.add_transaction(
        update.effective_user.id,
        parsed["amount"],
        parsed["type"],
        parsed["details"],
    )

async def weekly_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _report_command(update, context, "weekly")

async def monthly_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _report_command(update, context, "monthly")

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE, period: str):
    if not update.effective_user or not update.message:
        return

    db: Database = context.application.bot_data["database"]
    tz = context.application.bot_data["timezone"]

    report = build_report(db, update.effective_user.id, period, _now(tz))
    await update.message.reply_text(report)

async def error_handler(update, context):
    logger.error("Unhandled exception", exc_info=context.error)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("Set BOT_TOKEN environment variable.")

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
    app.add_error_handler(error_handler)

    app.post_init = set_commands
    setup_scheduler(app, db, tz)

    app.run_polling()

if __name__ == "__main__":
    main()
