"""Database module for managing transactions."""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import config


class Database:
    """Handles all database operations for the finance bot."""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        """Initialize the database connection."""
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create the transactions table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_transaction(self, user_id: int, amount: float, trans_type: str, category: str) -> bool:
        """
        Add a new transaction to the database.
        
        Args:
            user_id: Telegram user ID
            amount: Transaction amount
            trans_type: Transaction type (income/expense)
            category: Transaction category
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (user_id, amount, type, category, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, amount, trans_type, category, datetime.now()))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False
    
    def get_transactions(
        self, 
        user_id: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Get transactions for a user within a date range.
        
        Args:
            user_id: Telegram user ID
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
            
        Returns:
            List of transaction dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = 'SELECT * FROM transactions WHERE user_id = ?'
                params = [user_id]
                
                if start_date:
                    query += ' AND created_at >= ?'
                    params.append(start_date)
                
                if end_date:
                    query += ' AND created_at <= ?'
                    params.append(end_date)
                
                query += ' ORDER BY created_at DESC'
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def get_summary(
        self, 
        user_id: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get summary statistics for a user's transactions.
        
        Args:
            user_id: Telegram user ID
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
            
        Returns:
            Dictionary with income, expense, and balance
        """
        transactions = self.get_transactions(user_id, start_date, end_date)
        
        income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        
        return {
            'income': income,
            'expense': expense,
            'balance': income - expense,
            'transaction_count': len(transactions)
        }
