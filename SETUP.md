# Quick Setup Guide

## Prerequisites
- Python 3.7 or higher
- pip package manager
- A Telegram account

## Step-by-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create a Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Configure the Bot
Choose one of the following methods:

**Method A: Environment Variable (Recommended)**
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token-here"
```

**Method B: Edit config.py**
Open `config.py` and replace:
```python
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```
with your actual token:
```python
TELEGRAM_BOT_TOKEN = '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'
```

### 4. Run the Bot
```bash
python main.py
```

You should see:
```
INFO - Starting bot...
INFO - Bot initialized and scheduler started
```

### 5. Start Using the Bot
1. Open Telegram
2. Search for your bot by username (you set this with BotFather)
3. Send `/start` to begin
4. Start tracking your transactions!

## Usage Examples

### Recording Transactions
```
+ 1000 salary          → Records $1000 income
- 50 coffee            → Records $50 expense
+ 200 freelance work   → Records $200 income
- 1500 rent            → Records $1500 expense
```

### Viewing Reports
- `/daily` - Last 24 hours
- `/weekly` - Last 7 days  
- `/monthly` - Last 30 days

## Testing Without Telegram
Run the demo script to test all features locally:
```bash
python demo.py
```

## Customization

### Change Report Times
Edit `config.py`:
```python
DAILY_REPORT_TIME = '23:59'    # Daily at 11:59 PM
WEEKLY_REPORT_TIME = '23:59'   # Weekly on Sunday at 11:59 PM
MONTHLY_REPORT_TIME = '23:59'  # Monthly on last day at 11:59 PM
```

### Change Timezone
Edit `config.py`:
```python
TIMEZONE = 'America/New_York'  # or 'Europe/London', 'Asia/Tokyo', etc.
```

### Change Database Location
Edit `config.py`:
```python
DATABASE_PATH = '/path/to/your/database.db'
```

## Troubleshooting

### Bot doesn't respond
- Check that the bot token is correct
- Make sure `python main.py` is running
- Try sending `/start` command again

### Database errors
- Ensure write permissions in the directory
- Delete `finance_bot.db` to start fresh (this will delete all data)

### Import errors
- Run `pip install -r requirements.txt` again
- Ensure Python version is 3.7 or higher: `python --version`

## Support
For issues or questions, please open an issue on GitHub.
