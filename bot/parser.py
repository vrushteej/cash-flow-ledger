import re
from typing import Optional, TypedDict


class ParsedTransaction(TypedDict):
    amount: float
    type: str
    category: str


_TRANSACTION_RE = re.compile(
    r"^\s*([+-]?\d+(?:\.\d+)?)\s+(.+?)\s*$"
)


def parse_transaction(text: str) -> Optional[ParsedTransaction]:
    match = _TRANSACTION_RE.match(text or "")
    if not match:
        return None

    number_str, category = match.groups()

    try:
        amount = float(number_str)
    except ValueError:
        return None

    if amount == 0 or not category.strip():
        return None

    if amount > 0:
        tx_type = "income"
    else:
        tx_type = "expense"

    return {
        "amount": abs(amount),
        "type": tx_type,
        "category": category.strip(),
    }