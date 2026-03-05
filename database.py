from typing import Any, Dict, List
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self._conn = None
        self._connect()

    def _connect(self):
        """Create a new database connection."""
        self._conn = psycopg2.connect(
            self.database_url,
            sslmode="require"
        )

    def _ensure_connection(self):
        """Reconnect if connection is closed or broken."""
        try:
            if self._conn is None or self._conn.closed != 0:
                self._connect()
        except Exception:
            self._connect()

    def add_transaction(self, user_id: int, amount: float, tx_type: str, details: str) -> None:
        self._ensure_connection()

        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO transactions (user_id, amount, type, details)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, amount, tx_type, details.strip()),
                )
            self._conn.commit()

        except psycopg2.InterfaceError:
            # reconnect and retry
            self._connect()
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO transactions (user_id, amount, type, details)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, amount, tx_type, details.strip()),
                )
            self._conn.commit()

    def get_transactions_between(
        self, user_id: int, start, end
    ) -> List[Dict[str, Any]]:

        self._ensure_connection()

        try:
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

        except psycopg2.InterfaceError:
            self._connect()
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
        self._ensure_connection()

        try:
            with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT DISTINCT user_id FROM transactions")
                rows = cur.fetchall()
                return [int(row["user_id"]) for row in rows]

        except psycopg2.InterfaceError:
            self._connect()
            with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT DISTINCT user_id FROM transactions")
                rows = cur.fetchall()
                return [int(row["user_id"]) for row in rows]