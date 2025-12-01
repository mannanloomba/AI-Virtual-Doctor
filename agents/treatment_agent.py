# agents/treatment_agent.py
import asyncio
from typing import Dict, Any, List
from agents.knowledge_kb import KB
from tools.medication_safety import check_interactions, pregnancy_check, age_checks

class TreatmentAgent:
    def __init__(self):
        self.kb = {entry["id"]: entry for entry in KB}

    async def suggest(self, user_id: str, structured: Dict[str, Any], diagnosis: Dict[str, Any], patient_info: Dict[str, Any] = None) -> Dict[str, Any]:
        patient_info = patient_info or {}
        meds = []
        nonph = []
        follow_up_days = 3
        treatment_plan = []

        probs = diagnosis.get("probable_diagnoses", [])
        if not probs:
            # if no diagnosis, basic symptomatic care
            meds = ["paracetamol/acetaminophen"]
            nonph = ["rest", "hydration"]
            follow_up_days = 3
        else:
            for p in probs:
                pid = p["id"]
                entry = self.kb.get(pid)
                plan = entry.get("treatment", {}) if entry else {}
                tpl = {
                    "disease": entry["name"] if entry else p.get("name"),
                    "plan": {
                        "non_pharmacologic": plan.get("non_pharmacologic", []) if plan else [],
                        "first_line_medications": plan.get("medications", []) if plan else [],
                        "follow_up_days": p.get("follow_up_days", 5)
                    }
                }
                treatment_plan.append(tpl)
                for m in plan.get("medications", []):
                    meds.append(m)
                for n in plan.get("non_pharmacologic", []):
                    nonph.append(n)
                follow_up_days = max(follow_up_days, tpl["plan"]["follow_up_days"])

        # medication safety checks
        med_issues = check_interactions(meds)
        preg_warnings = pregnancy_check(meds) if patient_info.get("pregnant") else []
        age_warnings = age_checks(meds, patient_info.get("age"))

        medication_safety = {
            "interactions": med_issues,
            "pregnancy_warnings": preg_warnings,
            "age_warnings": age_warnings
        }

        await asyncio.sleep(0)
        return {
            "treatment_plan": treatment_plan,
            "medications": meds,
            "non_pharmacologic": list(dict.fromkeys(nonph)),
            "follow_up_days": follow_up_days,
            "notes": "",
            "medication_safety": medication_safety
        }
