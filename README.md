# Cash Flow Ledger 💰

Your financial co-pilot on Telegram. Turn your chat into a smart ledger that captures every gain and spend, delivering insightful daily, weekly, and monthly snapshots of your wealth.

## Features ✨

- 📝 **Easy Transaction Tracking**: Simply type `+ 100 salary` or `- 50 groceries`
- 📊 **Comprehensive Reports**: Get daily, weekly, and monthly financial summaries
- 🔔 **Automated Reports**: Receive scheduled reports automatically
- 💾 **SQLite Database**: All your data stored locally and securely
- ⚡ **Fast & Lightweight**: Built with Python and python-telegram-bot

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/vrushteej/cash-flow-ledger.git
   cd cash-flow-ledger
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your bot**
   
   Get a bot token from [@BotFather](https://t.me/botfather) on Telegram, then either:
   
   - Set an environment variable:
     ```bash
     export TELEGRAM_BOT_TOKEN="your-token-here"
     ```
   
   - Or edit `config.py` and replace `YOUR_BOT_TOKEN_HERE` with your token

4. **Run the bot**
   ```bash
   python main.py
   ```

## Usage 📖

### Recording Transactions

The bot supports a simple format for tracking your income and expenses:

**Income (use +)**
```
+ 1000 salary
+ 200 freelance work
+ 50 refund
```

**Expenses (use -)**
```
- 50 coffee
- 1500 rent
- 250 groceries
- 30 transport
```

### Commands

- `/start` - Start the bot and see welcome message
- `/help` - Get help on how to use the bot
- `/daily` - View transactions from the last 24 hours
- `/weekly` - View transactions from the last 7 days
- `/monthly` - View transactions from the last 30 days

### Automated Reports 🔔

The bot automatically sends reports:
- **Daily**: Every day at 11:59 PM
- **Weekly**: Every Sunday at 11:59 PM
- **Monthly**: On the last day of each month at 11:59 PM

## Project Structure 📁

```
cash-flow-ledger/
├── main.py          # Bot entry point and command handlers
├── parser.py        # Transaction message parser
├── database.py      # SQLite database operations
├── reports.py       # Report generation logic
├── scheduler.py     # Automated report scheduling
├── config.py        # Configuration settings
└── requirements.txt # Python dependencies
```

## Database Schema 💾

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    type TEXT NOT NULL,           -- 'income' or 'expense'
    category TEXT NOT NULL,        -- e.g., 'salary', 'groceries'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration ⚙️

Edit `config.py` to customize:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `DATABASE_PATH`: Path to SQLite database file (default: `finance_bot.db`)
- `TIMEZONE`: Timezone for scheduling (default: `UTC`)
- `DAILY_REPORT_TIME`: Time for daily reports (default: `23:59`)
- `WEEKLY_REPORT_TIME`: Time for weekly reports (default: `23:59`)
- `MONTHLY_REPORT_TIME`: Time for monthly reports (default: `23:59`)

## Example Report 📊

```
📊 Daily Report
Period: 2024-01-15 to 2024-01-16
==================================================

💰 Income: +$1200.00
💸 Expenses: -$350.00
📈 Balance: $850.00
📝 Transactions: 5

Detailed Transactions:
--------------------------------------------------
2024-01-15 14:30 | income | +$1000.00 | salary
2024-01-15 12:15 | expense | -$50.00 | lunch
2024-01-15 09:00 | expense | -$250.00 | groceries
2024-01-15 08:30 | expense | -$50.00 | transport
2024-01-16 10:00 | income | +$200.00 | freelance
```

## Technologies Used 🛠️

- **Python 3.x**: Core programming language
- **python-telegram-bot**: Telegram Bot API wrapper
- **SQLite**: Lightweight database
- **APScheduler**: Advanced Python Scheduler for automated reports

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the MIT License.

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.
