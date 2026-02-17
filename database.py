from typing import Any, Dict, List
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date

class Database:
    def __init__(self, database_url: str) -> None:
        if not database_url:
            raise RuntimeError("DATABASE_URL not set")
        self._conn = psycopg2.connect(database_url)

    def add_transaction(self, user_id: int, amount: float, tx_type: str, details: str) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions (user_id, amount, type, details)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, amount, tx_type, details.strip().lower()),
            )
        self._conn.commit()

    def get_transactions_between(
        self, user_id: int, start, end
    ) -> List[Dict[str, Any]]:
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, user_id, amount, type, details, created_at
                FROM transactions
                WHERE user_id = %s
                AND created_at >= %s
                AND created_at <= %s
                ORDER BY created_at ASC
                """,
                (user_id, start, end),
            )
            return cur.fetchall()

    def list_user_ids(self) -> List[int]:
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT DISTINCT user_id FROM transactions")
            return [int(row["user_id"]) for row in cur.fetchall()]
