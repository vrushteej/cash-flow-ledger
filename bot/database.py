import sqlite3
from typing import List


class Database:
    def __init__(self, path: str) -> None:
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

    def init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._conn.commit()

    def add_transaction(self, user_id: int, amount: float, tx_type: str, category: str) -> None:
        self._conn.execute(
            """
            INSERT INTO transactions (user_id, amount, type, category)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, amount, tx_type, category.strip().lower()),
        )
        self._conn.commit()

    def get_transactions_between(self, user_id: int, start_ts: str, end_ts: str) -> List[sqlite3.Row]:
        cur = self._conn.execute(
            """
            SELECT id, user_id, amount, type, category, created_at
            FROM transactions
            WHERE user_id = ? AND created_at >= ? AND created_at <= ?
            ORDER BY created_at ASC
            """,
            (user_id, start_ts, end_ts),
        )
        return cur.fetchall()

    def list_user_ids(self) -> List[int]:
        cur = self._conn.execute("SELECT DISTINCT user_id FROM transactions")
        return [row["user_id"] for row in cur.fetchall()]