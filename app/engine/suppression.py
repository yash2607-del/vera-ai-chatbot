import hashlib
from typing import Optional
from app.storage.suppression_store import SuppressionStore

class SuppressionEngine:
    def __init__(self, suppression_store: SuppressionStore):
        self.store = suppression_store

    @staticmethod
    def generate_suppression_key(merchant_id: str, signal_type: str, entity_id: Optional[str] = None) -> str:
        entity_str = entity_id or "default"
        raw_key = f"{merchant_id}:{signal_type}:{entity_str}"
        short_hash = hashlib.md5(raw_key.encode("utf-8")).hexdigest()[:8]
        return f"supp:{merchant_id}:{signal_type}:{short_hash}"

    def is_suppressed(self, suppression_key: str) -> bool:
        return self.store.is_suppressed(suppression_key)

    def record_suppression(self, suppression_key: str, merchant_id: str, signal_type: str, entity_id: Optional[str] = None):
        self.store.add_suppression(suppression_key, merchant_id, signal_type, entity_id)

    def clear(self, suppression_key: str):
        self.store.clear_suppression(suppression_key)
