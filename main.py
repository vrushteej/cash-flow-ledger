"""Main entry point for the Telegram Finance Bot."""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import config
from database import Database
from parser import TransactionParser
from reports import ReportGenerator
from scheduler import ReportScheduler


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize components
db = Database()
parser = TransactionParser()
report_gen = ReportGenerator(db)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user = update.effective_user
    welcome_message = (
        f"👋 Welcome {user.first_name}!\n\n"
        "I'm your personal finance tracking bot. Here's how to use me:\n\n"
        "📝 Track transactions:\n"
        "• Income: + 100 salary\n"
        "• Expense: - 250 groceries\n\n"
        "📊 View reports:\n"
        "/daily - Last 24 hours\n"
        "/weekly - Last 7 days\n"
        "/monthly - Last 30 days\n\n"
        "💡 I'll automatically send you reports:\n"
        "• Daily at 11:59 PM\n"
        "• Weekly on Sunday at 11:59 PM\n"
        "• Monthly on the last day at 11:59 PM\n\n"
        "Start tracking your finances now! 💰"
    )
    await update.message.reply_text(welcome_message)
    
    # Subscribe user to scheduled reports
    if hasattr(context.bot_data, 'scheduler'):
        context.bot_data['scheduler'].add_user(user.id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    help_message = (
        "📖 Help - How to use the Finance Bot\n\n"
        "💵 Recording Transactions:\n"
        "Use the following format to record transactions:\n"
        "• + <amount> <category> for income\n"
        "• - <amount> <category> for expenses\n\n"
        "Examples:\n"
        "• + 1000 salary\n"
        "• - 50 coffee\n"
        "• + 200 freelance\n"
        "• - 1500 rent\n\n"
        "📊 Viewing Reports:\n"
        "/daily - View transactions from the last 24 hours\n"
        "/weekly - View transactions from the last 7 days\n"
        "/monthly - View transactions from the last 30 days\n\n"
        "🔔 Automatic Reports:\n"
        "You'll receive reports automatically:\n"
        "• Daily at 11:59 PM\n"
        "• Weekly on Sunday at 11:59 PM\n"
        "• Monthly on the last day at 11:59 PM"
    )
    await update.message.reply_text(help_message)


async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /daily command."""
    user_id = update.effective_user.id
    report = report_gen.daily_report(user_id)
    await update.message.reply_text(report)


async def weekly_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /weekly command."""
    user_id = update.effective_user.id
    report = report_gen.weekly_report(user_id)
    await update.message.reply_text(report)


async def monthly_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /monthly command."""
    user_id = update.effective_user.id
    report = report_gen.monthly_report(user_id)
    await update.message.reply_text(report)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages (transactions)."""
    message_text = update.message.text
    user_id = update.effective_user.id
    
    # Try to parse as transaction
    result = parser.parse(message_text)
    
    if result is None:
        await update.message.reply_text(
            "❌ Invalid format!\n\n"
            "Use:\n"
            "• + <amount> <category> for income\n"
            "• - <amount> <category> for expenses\n\n"
            "Examples:\n"
            "• + 100 salary\n"
            "• - 50 groceries"
        )
        return
    
    trans_type, amount, category = result
    
    # Add to database
    success = db.add_transaction(user_id, amount, trans_type, category)
    
    if success:
        sign = '+' if trans_type == 'income' else '-'
        emoji = '💰' if trans_type == 'income' else '💸'
        await update.message.reply_text(
            f"✅ Transaction recorded!\n\n"
            f"{emoji} Type: {trans_type.capitalize()}\n"
            f"💵 Amount: {sign}${amount:.2f}\n"
            f"🏷️ Category: {category}"
        )
    else:
        await update.message.reply_text(
            "❌ Failed to record transaction. Please try again."
        )


async def post_init(application: Application):
    """Initialize scheduler after bot is ready."""
    scheduler = ReportScheduler(application.bot, db)
    scheduler.start()
    application.bot_data['scheduler'] = scheduler
    logger.info("Bot initialized and scheduler started")


async def post_shutdown(application: Application):
    """Clean up when bot shuts down."""
    if 'scheduler' in application.bot_data:
        application.bot_data['scheduler'].stop()
    logger.info("Bot shut down")


def main():
    """Start the bot."""
    # Check if token is configured
    if config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error(
            "Please set TELEGRAM_BOT_TOKEN in config.py or as an environment variable"
        )
        return
    
    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).post_init(post_init).post_shutdown(post_shutdown).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("daily", daily_command))
    application.add_handler(CommandHandler("weekly", weekly_command))
    application.add_handler(CommandHandler("monthly", monthly_command))
    
    # Add message handler for transactions
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
