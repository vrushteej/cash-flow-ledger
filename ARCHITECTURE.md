# Bot Architecture

## Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Telegram Users                          │
│              (Send messages, receive reports)               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                       main.py                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Bot Command Handlers:                                 │  │
│  │  • /start  - Welcome message                          │  │
│  │  • /help   - Usage instructions                       │  │
│  │  • /daily  - Daily report                             │  │
│  │  • /weekly - Weekly report                            │  │
│  │  • /monthly - Monthly report                          │  │
│  │  • Message handler - Parse transactions               │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────┬────────────────────┬─────────────────────────────┘
           │                    │
           ▼                    ▼
┌──────────────────┐   ┌──────────────────────┐
│   parser.py      │   │   scheduler.py       │
│                  │   │                      │
│ • Parse format:  │   │ • Daily: 11:59pm     │
│   "+ 100 salary" │   │ • Weekly: Sun 11:59pm│
│   "- 250 food"   │   │ • Monthly: Last day  │
│                  │   │                      │
│ • Extract:       │   │ • Auto-send reports  │
│   - Type         │   │   to subscribed      │
│   - Amount       │   │   users              │
│   - Category     │   │                      │
└────────┬─────────┘   └──────────┬───────────┘
         │                        │
         │                        │
         ▼                        ▼
┌──────────────────────────────────────────┐
│           database.py                    │
│  ┌────────────────────────────────────┐  │
│  │  SQLite Database Operations:       │  │
│  │  • init_db()                       │  │
│  │  • add_transaction()               │  │
│  │  • get_transactions()              │  │
│  │  • get_summary()                   │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Database: finance_bot.db                │
│  ┌────────────────────────────────────┐  │
│  │ Table: transactions                │  │
│  │ ┌────────────────────────────────┐ │  │
│  │ │ id (PK)                        │ │  │
│  │ │ user_id (INTEGER)              │ │  │
│  │ │ amount (REAL)                  │ │  │
│  │ │ type (TEXT)                    │ │  │
│  │ │ category (TEXT)                │ │  │
│  │ │ created_at (TIMESTAMP)         │ │  │
│  │ └────────────────────────────────┘ │  │
│  └────────────────────────────────────┘  │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│            reports.py                    │
│  ┌────────────────────────────────────┐  │
│  │  Report Generation:                │  │
│  │  • daily_report()                  │  │
│  │  • weekly_report()                 │  │
│  │  • monthly_report()                │  │
│  │  • format_transaction()            │  │
│  │                                    │  │
│  │  Output:                           │  │
│  │  • Summary (income/expense/balance)│  │
│  │  • Detailed transaction list       │  │
│  │  • Formatted with timestamps       │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘

Configuration: config.py
├── TELEGRAM_BOT_TOKEN
├── DATABASE_PATH
├── TIMEZONE
├── DAILY_REPORT_TIME
├── WEEKLY_REPORT_TIME
└── MONTHLY_REPORT_TIME
```

## Data Flow

### 1. Transaction Recording
```
User sends: "+ 100 salary"
    ↓
main.py receives message
    ↓
parser.py parses:
    - type: 'income'
    - amount: 100.0
    - category: 'salary'
    ↓
database.py stores:
    INSERT INTO transactions (
        user_id, amount, type, category, created_at
    ) VALUES (
        12345, 100.0, 'income', 'salary', '2024-01-15 14:30:00'
    )
    ↓
User receives confirmation
```

### 2. Manual Report Request
```
User sends: /daily
    ↓
main.py receives command
    ↓
reports.py generates report:
    - Query database for transactions
    - Calculate summary statistics
    - Format output with timestamps
    ↓
User receives formatted report
```

### 3. Automated Report Delivery
```
Scheduler triggers at 11:59pm
    ↓
scheduler.py executes:
    - For each subscribed user:
        ↓
    reports.py generates appropriate report
        ↓
    Bot sends report to user
```

## Technology Stack

- **Python 3.7+**: Core programming language
- **python-telegram-bot 20.7**: Telegram Bot API wrapper
- **SQLite**: Embedded database (no server needed)
- **APScheduler 3.10.4**: Advanced Python Scheduler

## Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Easy Configuration**: All settings in config.py
3. **Robust Parsing**: Transaction parser handles various formats
4. **Automatic Timestamps**: Database stores timestamps automatically
5. **Scheduled Automation**: Reports sent automatically at configured times
6. **User Privacy**: Each user's data is isolated by user_id
7. **Lightweight**: Minimal dependencies, SQLite database

## Error Handling

- Parser validates transaction format before processing
- Database operations wrapped in try-except blocks
- Scheduler continues on individual user failures
- Invalid transactions provide helpful error messages

## Security Features

- No hardcoded credentials (environment variables)
- Database file excluded from git (.gitignore)
- SQL injection protection (parameterized queries)
- Per-user data isolation
- No external API dependencies beyond Telegram
