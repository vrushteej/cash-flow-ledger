"""Reports module for generating transaction summaries."""
from datetime import datetime, timedelta
from typing import List, Dict
from database import Database


class ReportGenerator:
    """Generates financial reports for different time periods."""
    
    def __init__(self, db: Database):
        """Initialize the report generator with a database instance."""
        self.db = db
    
    def format_transaction(self, transaction: Dict) -> str:
        """
        Format a single transaction for display.
        
        Args:
            transaction: Transaction dictionary
            
        Returns:
            Formatted string
        """
        timestamp = transaction['created_at']
        trans_type = transaction['type']
        amount = transaction['amount']
        category = transaction['category']
        
        # Parse timestamp if it's a string
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except:
                timestamp = datetime.now()
        
        # Format: "2024-01-15 14:30 | income | $100.00 | salary"
        sign = '+' if trans_type == 'income' else '-'
        return f"{timestamp.strftime('%Y-%m-%d %H:%M')} | {trans_type} | {sign}${amount:.2f} | {category}"
    
    def generate_report(
        self, 
        user_id: int, 
        start_date: datetime,
        end_date: datetime,
        period_name: str
    ) -> str:
        """
        Generate a report for a specific time period.
        
        Args:
            user_id: Telegram user ID
            start_date: Start date for the report
            end_date: End date for the report
            period_name: Name of the period (e.g., "Daily", "Weekly")
            
        Returns:
            Formatted report string
        """
        transactions = self.db.get_transactions(user_id, start_date, end_date)
        summary = self.db.get_summary(user_id, start_date, end_date)
        
        # Build report header
        report = f"📊 {period_name} Report\n"
        report += f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n"
        report += "=" * 50 + "\n\n"
        
        # Add summary
        report += f"💰 Income: +${summary['income']:.2f}\n"
        report += f"💸 Expenses: -${summary['expense']:.2f}\n"
        report += f"📈 Balance: ${summary['balance']:.2f}\n"
        report += f"📝 Transactions: {summary['transaction_count']}\n\n"
        
        if transactions:
            report += "Detailed Transactions:\n"
            report += "-" * 50 + "\n"
            for transaction in transactions:
                report += self.format_transaction(transaction) + "\n"
        else:
            report += "No transactions found for this period.\n"
        
        return report
    
    def daily_report(self, user_id: int) -> str:
        """
        Generate a daily report (last 24 hours).
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Formatted report string
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        return self.generate_report(user_id, start_date, end_date, "Daily")
    
    def weekly_report(self, user_id: int) -> str:
        """
        Generate a weekly report (last 7 days).
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Formatted report string
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        return self.generate_report(user_id, start_date, end_date, "Weekly")
    
    def monthly_report(self, user_id: int) -> str:
        """
        Generate a monthly report (last 30 days).
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Formatted report string
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        return self.generate_report(user_id, start_date, end_date, "Monthly")
