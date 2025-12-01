# agents/diagnosis_agent.py
import asyncio
from typing import Dict, Any
from agents.knowledge_kb import KB

def _score_match(symptoms, kb_entry):
    # simple keyword overlap scoring
    text = " ".join(symptoms).lower()
    score = 0
    matched = 0
    for kw in kb_entry["keywords"]:
        if kw.lower() in text:
            matched += 1
    score = matched / max(1, len(kb_entry["keywords"]))
    return score, matched

class DiagnosisAgent:
    def __init__(self):
        # Could load a larger KB / models here
        self.kb = KB

    async def diagnose(self, user_id: str, structured: Dict[str, Any]) -> Dict[str, Any]:
        symptoms = structured.get("main_symptoms", [])
        results = []
        recommended_tests = set()

        for entry in self.kb:
            score, matched = _score_match(symptoms, entry)
            if matched > 0:
                results.append({
                    "id": entry["id"],
                    "name": entry["name"],
                    "score": round(score, 2),
                    "matched_keywords": matched,
                    "score_reason": f"Matched {matched} known keywords",
                    "recommended_tests": entry.get("tests", [])
                })
                for t in entry.get("tests", []):
                    recommended_tests.add(t)

        # sort by score desc, matched desc
        results = sorted(results, key=lambda r: (-r["score"], -r["matched_keywords"]))
        reasoning = "Rule-based knowledge matching from small KB"
        await asyncio.sleep(0)  # keep async-friendly
        return {
            "probable_diagnoses": results,
            "recommended_tests": list(recommended_tests),
            "reasoning": reasoning
        }
