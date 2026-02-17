"""Scheduler module for automated report delivery."""
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot
from typing import Set
import config
from reports import ReportGenerator
from database import Database


class ReportScheduler:
    """Handles scheduled report delivery to users."""
    
    def __init__(self, bot: Bot, db: Database):
        """
        Initialize the scheduler.
        
        Args:
            bot: Telegram Bot instance
            db: Database instance
        """
        self.bot = bot
        self.db = db
        self.report_generator = ReportGenerator(db)
        self.scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
        self.subscribed_users: Set[int] = set()
    
    def add_user(self, user_id: int):
        """Add a user to receive scheduled reports."""
        self.subscribed_users.add(user_id)
    
    def remove_user(self, user_id: int):
        """Remove a user from scheduled reports."""
        self.subscribed_users.discard(user_id)
    
    async def send_daily_reports(self):
        """Send daily reports to all subscribed users."""
        for user_id in self.subscribed_users:
            try:
                report = self.report_generator.daily_report(user_id)
                await self.bot.send_message(chat_id=user_id, text=report)
            except Exception as e:
                print(f"Error sending daily report to user {user_id}: {e}")
    
    async def send_weekly_reports(self):
        """Send weekly reports to all subscribed users."""
        for user_id in self.subscribed_users:
            try:
                report = self.report_generator.weekly_report(user_id)
                await self.bot.send_message(chat_id=user_id, text=report)
            except Exception as e:
                print(f"Error sending weekly report to user {user_id}: {e}")
    
    async def send_monthly_reports(self):
        """Send monthly reports to all subscribed users."""
        for user_id in self.subscribed_users:
            try:
                report = self.report_generator.monthly_report(user_id)
                await self.bot.send_message(chat_id=user_id, text=report)
            except Exception as e:
                print(f"Error sending monthly report to user {user_id}: {e}")
    
    def start(self):
        """Start the scheduler with all report jobs."""
        # Parse time from config
        daily_hour, daily_minute = map(int, config.DAILY_REPORT_TIME.split(':'))
        weekly_hour, weekly_minute = map(int, config.WEEKLY_REPORT_TIME.split(':'))
        monthly_hour, monthly_minute = map(int, config.MONTHLY_REPORT_TIME.split(':'))
        
        # Schedule daily report (every day at specified time)
        self.scheduler.add_job(
            self.send_daily_reports,
            CronTrigger(hour=daily_hour, minute=daily_minute),
            id='daily_report'
        )
        
        # Schedule weekly report (every Sunday at specified time)
        self.scheduler.add_job(
            self.send_weekly_reports,
            CronTrigger(day_of_week='sun', hour=weekly_hour, minute=weekly_minute),
            id='weekly_report'
        )
        
        # Schedule monthly report (last day of month at specified time)
        self.scheduler.add_job(
            self.send_monthly_reports,
            CronTrigger(day='last', hour=monthly_hour, minute=monthly_minute),
            id='monthly_report'
        )
        
        self.scheduler.start()
        print("Scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        print("Scheduler stopped")
