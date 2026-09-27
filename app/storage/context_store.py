import json
import sqlite3
from typing import Optional, Dict, Any, Union
from app.models.context import ContextPayload, ContextStoreRecord
from app.core.logging import logger

def parse_version(v: Union[int, float, str]) -> float:
    try:
        return float(v)
    except ValueError:
        # Handle string formats like "1.2" or "v1.0"
        cleaned = str(v).lower().lstrip("v").strip()
        parts = cleaned.split(".")
        if len(parts) >= 2:
            return float(f"{parts[0]}.{parts[1]}")
        elif len(parts) == 1 and parts[0].isdigit():
            return float(parts[0])
        return 1.0

class ContextStore:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def upsert_context(self, payload: ContextPayload) -> Dict[str, Any]:
        v_num = parse_version(payload.version)
        cursor = self.conn.cursor()
        
        # Check existing version
        cursor.execute(
            "SELECT version_num, version_raw FROM context_store WHERE scope = ? AND context_id = ?",
            (payload.scope, payload.context_id)
        )
        row = cursor.fetchone()
        
        if row:
            existing_v_num = row["version_num"]
            if v_num <= existing_v_num:
                logger.info(f"Skipping context update for scope={payload.scope}, id={payload.context_id}: incoming version {payload.version} <= existing version {row['version_raw']}")
                return {
                    "status": "skipped",
                    "reason": f"Incoming version {payload.version} is not newer than existing version {row['version_raw']}"
                }
        
        data_json = json.dumps(payload.data)
        cursor.execute("""
            INSERT INTO context_store (scope, context_id, version_num, version_raw, data_json, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(scope, context_id) DO UPDATE SET
                version_num = excluded.version_num,
                version_raw = excluded.version_raw,
                data_json = excluded.data_json,
                updated_at = CURRENT_TIMESTAMP
        """, (payload.scope, payload.context_id, v_num, str(payload.version), data_json))
        self.conn.commit()
        
        action = "updated" if row else "created"
        return {"status": action, "version": str(payload.version)}

    def get_context(self, scope: str, context_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT data_json FROM context_store WHERE scope = ? AND context_id = ?",
            (scope, context_id)
        )
        row = cursor.fetchone()
        if row and row["data_json"]:
            return json.loads(row["data_json"])
        return None
