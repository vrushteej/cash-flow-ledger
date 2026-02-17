import re
from typing import Optional, TypedDict

class ParsedTransaction(TypedDict):
    amount: float
    type: str
    details: str

_TRANSACTION_RE = re.compile(
    r"^\s*([+-]?\d+(?:\.\d+)?)\s+(.+?)\s*$"
)

def parse_transaction(text: str) -> Optional[ParsedTransaction]:
    match = _TRANSACTION_RE.match(text or "")
    if not match:
        return None

    number_str, details = match.groups()

    try:
        amount = float(number_str)
    except ValueError:
        return None

    if amount == 0:
        return None

    tx_type = "income" if amount > 0 else "expense"

    return {
        "amount": abs(amount),
        "type": tx_type,
        "details": details.strip(),
    }