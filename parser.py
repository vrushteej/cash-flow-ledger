"""Parser module for transaction messages."""
import re
from typing import Optional, Tuple


class TransactionParser:
    """Parses transaction messages in the format '+ 100 salary' or '- 250 groceries'."""
    
    @staticmethod
    def parse(message: str) -> Optional[Tuple[str, float, str]]:
        """
        Parse a transaction message.
        
        Expected formats:
        - "+ 100 salary" (income)
        - "- 250 groceries" (expense)
        - "+100 salary" (without space after sign)
        - "-250 groceries" (without space after sign)
        
        Args:
            message: The message to parse
            
        Returns:
            Tuple of (type, amount, category) or None if invalid
        """
        # Remove extra whitespace
        message = message.strip()
        
        # Pattern: optional +/-, amount, category
        # Matches: "+ 100 salary", "- 250 groceries", "+100 salary", "-250 groceries"
        pattern = r'^([+-])\s*(\d+(?:\.\d+)?)\s+(.+)$'
        match = re.match(pattern, message)
        
        if not match:
            return None
        
        sign, amount, category = match.groups()
        
        # Determine transaction type
        trans_type = 'income' if sign == '+' else 'expense'
        
        # Convert amount to float
        try:
            amount = float(amount)
        except ValueError:
            return None
        
        # Clean up category
        category = category.strip()
        
        if not category:
            return None
        
        return (trans_type, amount, category)
    
    @staticmethod
    def is_valid_transaction(message: str) -> bool:
        """
        Check if a message is a valid transaction.
        
        Args:
            message: The message to validate
            
        Returns:
            True if valid transaction, False otherwise
        """
        return TransactionParser.parse(message) is not None
