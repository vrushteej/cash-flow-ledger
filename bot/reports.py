from datetime import datetime, timedelta
from typing import Tuple

from database import Database

def get_period_bounds(period: str, now: datetime) -> Tuple[datetime, datetime, str]:
    period = period.lower()

    if period == "daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        title = "Daily Summary"
    elif period == "weekly":
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start = start_of_day - timedelta(days=now.weekday())
        title = "Weekly Summary"
    elif period == "monthly":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        title = "Monthly Summary"
    else:
        raise ValueError(f"Unsupported period: {period}")

    return start, now, title

def build_report(database: Database, user_id: int, period: str, now: datetime) -> str:
    start, end, _ = get_period_bounds(period, now)
    rows, income_total, expense_total = collect_transactions(database, user_id, start, end)

    date_format = "%d-%m-%Y"
    time_format = "%H:%M"

    if period == "daily":
        header = f"{start.strftime(date_format)}"
    else:
        header = f"{start.strftime(date_format)} to {end.strftime(date_format)}"

    lines = [header, ""]

    # For daily → show only time
    # For weekly/monthly → show date + time
    for row in rows:
        dt = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S")

        if period == "daily":
            dt_str = dt.strftime(time_format)
        else:
            dt_str = dt.strftime(f"{date_format} {time_format}")

        tx_label = "received" if row["type"] == "income" else "expense"

        lines.append(
            f"{dt_str} | {tx_label} | Rs. {float(row['amount']):.0f} | {row['category']}"
        )

    lines.append("")
    lines.append(f"Income: Rs. {income_total:.0f}")
    lines.append(f"Expense: Rs. {expense_total:.0f}")

    return "\n".join(lines)

def collect_transactions(database: Database, user_id: int, start: datetime, end: datetime):
    rows = database.get_transactions_between(
        user_id,
        start.strftime("%Y-%m-%d %H:%M:%S"),
        end.strftime("%Y-%m-%d %H:%M:%S"),
    )

    income_total = 0.0
    expense_total = 0.0

    for row in rows:
        amount = float(row["amount"])
        if row["type"] == "income":
            income_total += amount
        else:
            expense_total += amount

    return rows, income_total, expense_total

def build_summary(database: Database, user_id: int, period: str, now: datetime) -> str:
    start, end, _ = get_period_bounds(period, now)
    rows, income_total, expense_total = collect_transactions(database, user_id, start, end)

    date_format = "%d-%m-%Y"

    if period == "daily":
        header = f"{start.strftime(date_format)}"
    else:
        header = f"{start.strftime(date_format)} to {end.strftime(date_format)}"

    lines = [
        header,
        "",
        f"Income: Rs. {income_total:.0f}",
        f"Expense: Rs. {expense_total:.0f}",
    ]

    return "\n".join(lines)
