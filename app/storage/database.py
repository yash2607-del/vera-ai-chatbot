import sqlite3
import os
from typing import Generator
from app.core.config import settings

def get_db_path() -> str:
    path = settings.DATABASE_PATH
    if path.startswith("sqlite:///"):
        path = path.replace("sqlite:///", "")
    return os.path.abspath(path)

def init_db():
    db_file = get_db_path()
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Context Store Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS context_store (
            scope TEXT NOT NULL,
            context_id TEXT NOT NULL,
            version_num REAL NOT NULL,
            version_raw TEXT NOT NULL,
            data_json TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (scope, context_id)
        );
    """)
    
    # Suppression Store Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppression_store (
            suppression_key TEXT PRIMARY KEY,
            merchant_id TEXT NOT NULL,
            signal_type TEXT NOT NULL,
            entity_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Conversation Store Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_store (
            conversation_id TEXT PRIMARY KEY,
            merchant_id TEXT NOT NULL,
            state TEXT NOT NULL,
            last_signal_type TEXT,
            last_evidence_json TEXT,
            last_message TEXT,
            last_cta TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    conn.close()

def get_db():
    db_file = get_db_path()
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
