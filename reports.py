from datetime import datetime, timedelta
from typing import Tuple
from database import Database


def get_period_bounds(period: str, now: datetime) -> Tuple[datetime, datetime]:
    period = period.lower()

    if period == "daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start -= timedelta(days=now.weekday())
    elif period == "monthly":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        raise ValueError("Invalid period")

    return start, now


def build_report(database: Database, user_id: int, period: str, now: datetime) -> str:
    start, end = get_period_bounds(period, now)
    rows = database.get_transactions_between(user_id, start, end)

    income_total = 0.0
    expense_total = 0.0

    date_format = "%d-%m-%Y"
    time_format = "%H:%M"

    if period == "daily":
        header = start.strftime(date_format)
    else:
        header = f"{start.strftime(date_format)} to {end.strftime(date_format)}"

    lines = [header, ""]

    for row in rows:
        dt = row["created_at"].astimezone(now.tzinfo)

        if period == "daily":
            dt_str = dt.strftime(time_format)
        else:
            dt_str = dt.strftime(f"{date_format} {time_format}")

        label = "received" if row["type"] == "income" else "expense"

        amount = float(row["amount"])

        if row["type"] == "income":
            income_total += amount
        else:
            expense_total += amount

        lines.append(
            f"{dt_str} | {label} | Rs. {amount:.2f} | {row['details']}"
        )

    lines.append("")
    lines.append(f"Income: Rs. {income_total:.2f}")
    lines.append(f"Expense: Rs. {expense_total:.2f}")

    return "\n".join(lines)


def build_summary(database: Database, user_id: int, period: str, now: datetime) -> str:
    start, end = get_period_bounds(period, now)
    rows = database.get_transactions_between(user_id, start, end)

    income_total = 0.0
    expense_total = 0.0

    for row in rows:
        amount = float(row["amount"])
        if row["type"] == "income":
            income_total += amount
        else:
            expense_total += amount

    date_format = "%d-%m-%Y"

    if period == "daily":
        header = start.strftime(date_format)
    else:
        header = f"{start.strftime(date_format)} to {end.strftime(date_format)}"

    return (
        f"{header}\n\n"
        f"Income: Rs. {income_total:.2f}\n"
        f"Expense: Rs. {expense_total:.2f}"
    )
