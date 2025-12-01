# tools/medication_safety.py
# Lightweight medication safety tool (local, simple DB)
# Not exhaustive. For demo/competition only.

INTERACTIONS = {
    ("ibuprofen", "warfarin"): "Increased bleeding risk.",
    ("aspirin", "warfarin"): "Increased bleeding risk.",
    ("paracetamol", "alcohol"): "Liver risk with chronic alcohol use.",
}

PREGNANCY_WARNINGS = {
    "ibuprofen": "Avoid in pregnancy (especially 3rd trimester).",
    "warfarin": "Contraindicated in pregnancy.",
}

AGE_WARNINGS = {
    "aspirin": "Not recommended in children with viral illness (Reye's syndrome risk)."
}

def check_interactions(med_list):
    med_set = [m.lower() for m in med_list]
    issues = []
    for i in range(len(med_set)):
        for j in range(i+1, len(med_set)):
            pair = (med_set[i], med_set[j])
            pair_rev = (med_set[j], med_set[i])
            if pair in INTERACTIONS:
                issues.append({"pair": pair, "issue": INTERACTIONS[pair]})
            elif pair_rev in INTERACTIONS:
                issues.append({"pair": pair_rev, "issue": INTERACTIONS[pair_rev]})
    return issues

def pregnancy_check(med_list):
    warnings = []
    for m in med_list:
        if m.lower() in PREGNANCY_WARNINGS:
            warnings.append({"med": m, "warning": PREGNANCY_WARNINGS[m.lower()]})
    return warnings

def age_checks(med_list, age=None):
    warnings = []
    for m in med_list:
        if m.lower() in AGE_WARNINGS:
            warnings.append({"med": m, "warning": AGE_WARNINGS[m.lower()]})
    return warnings
