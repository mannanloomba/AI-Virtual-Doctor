# backend/session_service.py
import os
import json
import uuid
from pathlib import Path
from typing import Dict, Any

STORAGE_DIR = Path.cwd() / "memory_storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
SESSION_FILE = STORAGE_DIR / "sessions.json"

def _read_all():
    if not SESSION_FILE.exists():
        return {}
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def _write_all(data):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class SessionService:
    def __init__(self):
        self.store = _read_all()

    def create_session(self, user_id: str) -> str:
        sid = str(uuid.uuid4())
        self.store[sid] = {"user_id": user_id, "entries": []}
        _write_all(self.store)
        return sid

    def append(self, session_id: str, entry: Dict[str, Any]):
        if session_id not in self.store:
            # create a fallback session
            self.store[session_id] = {"user_id": entry.get("user_id", "unknown"), "entries": []}
        self.store[session_id]["entries"].append(entry)
        _write_all(self.store)

    def get_session(self, session_id: str):
        return self.store.get(session_id)
