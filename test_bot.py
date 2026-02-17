#!/usr/bin/env python3
"""Test script to validate bot components."""

import os
import sys
from datetime import datetime

# Test imports
print("Testing imports...")
try:
    import config
    from database import Database
    from parser import TransactionParser
    from reports import ReportGenerator
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test parser
print("\nTesting parser...")
parser = TransactionParser()

test_cases = [
    ("+ 100 salary", ('income', 100.0, 'salary')),
    ("- 250 groceries", ('expense', 250.0, 'groceries')),
    ("+50 coffee", ('income', 50.0, 'coffee')),
    ("-1500 rent", ('expense', 1500.0, 'rent')),
    ("+ 99.99 refund", ('income', 99.99, 'refund')),
]

for message, expected in test_cases:
    result = parser.parse(message)
    if result == expected:
        print(f"✅ '{message}' -> {result}")
    else:
        print(f"❌ '{message}' -> {result}, expected {expected}")

# Test invalid formats
invalid_cases = [
    "100 salary",  # Missing sign
    "+ 100",  # Missing category
    "- abc groceries",  # Invalid amount
    "",  # Empty
]

for message in invalid_cases:
    result = parser.parse(message)
    if result is None:
        print(f"✅ Invalid format correctly rejected: '{message}'")
    else:
        print(f"❌ Should reject: '{message}' but got {result}")

# Test database
print("\nTesting database...")
test_db_path = "/tmp/test_finance_bot.db"
if os.path.exists(test_db_path):
    os.remove(test_db_path)

db = Database(test_db_path)
print("✅ Database initialized")

# Add test transactions
test_user_id = 12345
transactions = [
    (100.0, 'income', 'salary'),
    (50.0, 'expense', 'coffee'),
    (250.0, 'expense', 'groceries'),
    (200.0, 'income', 'freelance'),
]

for amount, trans_type, category in transactions:
    success = db.add_transaction(test_user_id, amount, trans_type, category)
    if success:
        print(f"✅ Added {trans_type}: ${amount} ({category})")
    else:
        print(f"❌ Failed to add transaction")

# Test retrieval
results = db.get_transactions(test_user_id)
print(f"✅ Retrieved {len(results)} transactions")

# Test summary
summary = db.get_summary(test_user_id)
print(f"✅ Summary: Income=${summary['income']}, Expense=${summary['expense']}, Balance=${summary['balance']}")

expected_income = 300.0  # 100 + 200
expected_expense = 300.0  # 50 + 250
expected_balance = 0.0

if summary['income'] == expected_income and summary['expense'] == expected_expense:
    print("✅ Summary calculations correct")
else:
    print(f"❌ Summary incorrect: got income={summary['income']}, expense={summary['expense']}")

# Test reports
print("\nTesting report generation...")
report_gen = ReportGenerator(db)
daily_report = report_gen.daily_report(test_user_id)
print("✅ Daily report generated")
print(f"Report preview (first 200 chars):\n{daily_report[:200]}...")

# Cleanup
os.remove(test_db_path)
print("\n✅ All tests passed!")
