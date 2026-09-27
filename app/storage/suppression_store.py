import sqlite3
from typing import Optional
from app.core.config import settings

class SuppressionStore:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def is_suppressed(self, suppression_key: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT created_at FROM suppression_store WHERE suppression_key = ?",
            (suppression_key,)
        )
        row = cursor.fetchone()
        return row is not None

    def add_suppression(self, suppression_key: str, merchant_id: str, signal_type: str, entity_id: Optional[str] = None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO suppression_store (suppression_key, merchant_id, signal_type, entity_id, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (suppression_key, merchant_id, signal_type, entity_id or ""))
        self.conn.commit()

    def clear_suppression(self, suppression_key: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM suppression_store WHERE suppression_key = ?", (suppression_key,))
        self.conn.commit()
