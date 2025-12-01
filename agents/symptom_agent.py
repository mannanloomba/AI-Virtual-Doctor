# agents/symptom_agent.py
import re, json
from typing import Dict, Any
from backend.session_service import SessionService

# Use local rule-based extraction only (robust, no external dependency required)
def clean_symptom_text(text: str):
    text = text.strip()
    text = re.sub(r"(^i have|^i'm|^i am|^i had|^i feel)\s+", "", text, flags=re.I)
    text = re.sub(r"\bfor\s+\d+\s*(day|days|d|hr|hrs|hours)\b", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_into_symptoms(text: str):
    parts = re.split(r"[,;]| and | & | then | but ", text, flags=re.I)
    symptoms = []
    for p in parts:
        p = clean_symptom_text(p)
        if p:
            symptoms.append(p)
    # dedupe preserving order
    return list(dict.fromkeys(symptoms))

def extract_duration(text):
    m = re.search(r"(\d+)\s*(day|days|d)", text.lower())
    if m:
        return int(m.group(1))
    return None

def extract_temperature(text: str):
    m = re.search(r"(\d{2,3}(?:\.\d+)?)\s*(?:°|deg|degree)?\s*([cf]?)", text.lower())
    if not m:
        return None, None
    val = float(m.group(1))
    unit = m.group(2) or ""
    if unit == "":
        if 30 <= val <= 45:
            unit = "c"
        elif 95 <= val <= 110:
            unit = "f"
    if unit == "f":
        temp_c = (val - 32) * 5 / 9
    else:
        temp_c = val
    return round(temp_c, 1), unit or "unknown"

def rule_based_severity(main_symptoms, duration_days, red_flags):
    main = " ".join(main_symptoms).lower()
    red = " ".join(red_flags).lower()
    serious = ["chest pain", "shortness of breath", "seizure", "unconscious", "confusion", "vomiting blood"]
    for s in serious:
        if s in main or s in red:
            return "severe"
    if duration_days is not None:
        if duration_days >= 7:
            return "severe"
        if duration_days >= 3:
            return "moderate"
    if len(main_symptoms) >= 3:
        return "moderate"
    return "mild"

class SymptomAgent:
    def __init__(self, session_service: SessionService):
        self.session_service = session_service

    async def parse_symptoms(self, user_id: str, text: str) -> Dict[str, Any]:
        text = text or ""
        main_symptoms = split_into_symptoms(text)
        duration = extract_duration(text)
        temp_c, temp_unit = extract_temperature(text)

        data = {
            "main_symptoms": main_symptoms,
            "duration_days": duration,
            "severity": "",
            "possible_causes": [],
            "red_flags": []
        }
        if temp_c is not None:
            data["temperature_celsius"] = temp_c

        # severity fallback
        data["severity"] = rule_based_severity(data["main_symptoms"], data["duration_days"], data["red_flags"])

        session_id = self.session_service.create_session(user_id)
        entry = {"user_id": user_id, "input_text": text, "structured": data}
        self.session_service.append(session_id, entry)

        return {"session_id": session_id, "structured": data}
