# agents/triage_agent.py
def assess_triage(structured: dict) -> dict:
    severity = structured.get("severity", "")
    duration = structured.get("duration_days", 0) or 0
    temp = structured.get("temperature_celsius", None)
    red_flags = structured.get("red_flags", [])

    level = "self-care"
    reasons = []

    # basic rule-set
    if "severe" in severity:
        level = "emergency"
        reasons.append("Severe symptoms detected.")
    elif duration >= 7:
        level = "urgent-care"
        reasons.append("Symptoms lasting 7+ days.")
    elif temp is not None and temp >= 40.5:
        level = "urgent-care"
        reasons.append("Very high temperature.")
    elif len(structured.get("main_symptoms", [])) >= 3:
        level = "urgent-care"
        reasons.append("Multiple symptoms present.")
    else:
        level = "self-care"
        reasons.append("Mild symptoms or insufficient data")

    confidence = 0.8
    return {"level": level, "reasons": reasons, "confidence": confidence}
