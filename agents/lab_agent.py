# agents/lab_agent.py
from typing import Dict, Any

class LabAgent:
    def __init__(self):
        pass

    def recommended_tests_for(self, diagnoses: Dict[str, Any]):
        tests = []
        for p in diagnoses.get("probable_diagnoses", []):
            tests.extend(p.get("recommended_tests", []))
        return list(dict.fromkeys(tests))
