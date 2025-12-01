# agents/prescription_agent.py
import uuid
from typing import Dict, Any

class PrescriptionAgent:
    def __init__(self):
        pass

    def create_prescription(self, user_id: str, treatment: Dict[str, Any]) -> Dict[str, Any]:
        prescription_id = str(uuid.uuid4())
        meds = treatment.get("medications", [])
        notes = treatment.get("notes", "")
        return {
            "prescription_id": prescription_id,
            "user_id": user_id,
            "medications": meds,
            "notes": notes
        }
