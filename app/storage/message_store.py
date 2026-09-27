import json
import sqlite3
from typing import Optional, Dict, Any
from app.models.conversation import ConversationRecord
from app.core.constants import ConversationState

class MessageStore:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_conversation(self, conversation_id: str) -> Optional[ConversationRecord]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM conversation_store WHERE conversation_id = ?",
            (conversation_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
            
        evidence = json.loads(row["last_evidence_json"]) if row["last_evidence_json"] else None
        return ConversationRecord(
            conversation_id=row["conversation_id"],
            merchant_id=row["merchant_id"],
            state=ConversationState(row["state"]),
            last_signal_type=row["last_signal_type"],
            last_evidence=evidence,
            last_message=row["last_message"],
            last_cta=row["last_cta"],
            updated_at=row["updated_at"]
        )

    def save_conversation(self, record: ConversationRecord):
        cursor = self.conn.cursor()
        evidence_json = json.dumps(record.last_evidence) if record.last_evidence else None
        cursor.execute("""
            INSERT INTO conversation_store (
                conversation_id, merchant_id, state, last_signal_type, last_evidence_json, last_message, last_cta, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(conversation_id) DO UPDATE SET
                state = excluded.state,
                last_signal_type = excluded.last_signal_type,
                last_evidence_json = excluded.last_evidence_json,
                last_message = excluded.last_message,
                last_cta = excluded.last_cta,
                updated_at = CURRENT_TIMESTAMP
        """, (
            record.conversation_id,
            record.merchant_id,
            record.state.value,
            record.last_signal_type,
            evidence_json,
            record.last_message,
            record.last_cta
        ))
        self.conn.commit()
