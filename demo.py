"""
Demonstration script showing how the bot components work together.
This simulates the bot's core functionality without requiring a Telegram connection.
"""

from datetime import datetime, timedelta
from database import Database
from parser import TransactionParser
from reports import ReportGenerator

print("=" * 70)
print("TELEGRAM FINANCE BOT - DEMONSTRATION")
print("=" * 70)

# Initialize components
print("\n1. Initializing bot components...")
db = Database('/tmp/demo_finance_bot.db')
parser = TransactionParser()
report_gen = ReportGenerator(db)
print("✅ Database, Parser, and Report Generator initialized")

# Simulate a user
user_id = 123456
print(f"\n2. Simulating user (ID: {user_id})")

# Parse and add sample transactions
print("\n3. Adding sample transactions...")
sample_messages = [
    "+ 3000 salary",
    "- 50 coffee",
    "- 1200 rent",
    "+ 500 freelance",
    "- 80 groceries",
    "- 30 transport",
    "+ 100 refund",
    "- 45 entertainment",
]

print("\nTransaction Messages:")
for msg in sample_messages:
    result = parser.parse(msg)
    if result:
        trans_type, amount, category = result
        success = db.add_transaction(user_id, amount, trans_type, category)
        sign = '+' if trans_type == 'income' else '-'
        status = '✅' if success else '❌'
        print(f"  {status} {msg:20s} -> {trans_type:7s} {sign}${amount:8.2f} ({category})")

# Generate and display summary
print("\n4. Generating Financial Summary...")
summary = db.get_summary(user_id)
print(f"\n{'='*50}")
print(f"💰 Total Income:     ${summary['income']:>10,.2f}")
print(f"💸 Total Expenses:   ${summary['expense']:>10,.2f}")
print(f"{'='*50}")
print(f"📈 Net Balance:      ${summary['balance']:>10,.2f}")
print(f"📝 Transactions:     {summary['transaction_count']:>10}")
print(f"{'='*50}")

# Generate reports
print("\n5. Generating Reports...")

print("\n" + "─" * 70)
print("DAILY REPORT (Last 24 hours)")
print("─" * 70)
daily = report_gen.daily_report(user_id)
print(daily)

print("\n" + "─" * 70)
print("WEEKLY REPORT (Last 7 days)")
print("─" * 70)
weekly = report_gen.weekly_report(user_id)
print(weekly)

print("\n" + "─" * 70)
print("MONTHLY REPORT (Last 30 days)")
print("─" * 70)
monthly = report_gen.monthly_report(user_id)
print(monthly)

# Show transaction parsing examples
print("\n" + "=" * 70)
print("6. TRANSACTION PARSING EXAMPLES")
print("=" * 70)

examples = [
    ("+ 1000 salary", "✅ Valid income"),
    ("- 250 groceries", "✅ Valid expense"),
    ("+50.99 bonus", "✅ Valid with decimal"),
    ("100 coffee", "❌ Missing +/- sign"),
    ("+ 100", "❌ Missing category"),
]

print("\nFormat: [sign] [amount] [category]")
print("\nExamples:")
for msg, description in examples:
    result = parser.parse(msg)
    status = "VALID" if result else "INVALID"
    print(f"  '{msg:20s}' -> {status:8s} ({description})")

print("\n" + "=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)
print("\nThe bot is ready to use! To start:")
print("1. Get a bot token from @BotFather on Telegram")
print("2. Set TELEGRAM_BOT_TOKEN in config.py or as environment variable")
print("3. Run: python main.py")
print("4. Start chatting with your bot on Telegram!")
print("\nCommands: /start, /help, /daily, /weekly, /monthly")
print("=" * 70)

# Cleanup
import os
os.remove('/tmp/demo_finance_bot.db')
