# memory/memory_service.py
import json
from pathlib import Path

MEM_FILE = Path.cwd() / "memory_storage" / "memory.json"
MEM_FILE.parent.mkdir(parents=True, exist_ok=True)
if not MEM_FILE.exists():
    MEM_FILE.write_text(json.dumps({}, indent=2))

class MemoryService:
    def __init__(self):
        self._load()

    def _load(self):
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            try:
                self.storage = json.load(f)
            except:
                self.storage = {}

    def _save(self):
        with open(MEM_FILE, "w", encoding="utf-8") as f:
            json.dump(self.storage, f, indent=2)

    def add_medical_history(self, user_id: str, record: dict):
        user = self.storage.setdefault(user_id, {"history": []})
        user["history"].append(record)
        self._save()

    def add_image_record(self, user_id, record):
        self.storage.setdefault(user_id, {}).setdefault("images", []).append(record)
        self._save()

    def get_last_image_analysis(self, user_id):
        imgs = self.storage.get(user_id, {}).get("images", [])
        return imgs[-1] if imgs else None

    def get_history(self, user_id: str):
        # Ensure we return a flat list of records
        raw = self.storage.get(user_id, {}).get("history", [])
        # If double nested (legacy), flatten it
        clean = []
        for r in raw:
            if "record" in r and isinstance(r["record"], dict):
                # It was nested like {"record": {"time":..., "record":...}}
                clean.append(r["record"])
            else:
                clean.append(r)
        return clean
