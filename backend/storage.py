# backend/storage.py
import json
import os

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "memory_storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

def save_session(session_id: str, data: dict):
    path = os.path.join(STORAGE_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_session(session_id: str):
    path = os.path.join(STORAGE_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
