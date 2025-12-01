

from pydantic import BaseModel
from typing import Optional, List

# Structured symptom input (after parsing)
class SymptomStruct(BaseModel):
    user_id: str
    symptoms: List[str]
    duration_days: Optional[int] = None
    severity: Optional[str] = None
    notes: Optional[str] = None

# Output for triage
class TriageResult(BaseModel):
    level: str              # e.g., "self-care", "consult", "urgent"
    reasons: List[str]      # explanation for triage
    confidence: float       # later from AI model or rules

# Image analysis result structure
class ImageAnalysis(BaseModel):
    user_id: str
    filename: str
    analysis: str           # placeholder: "rash detected", etc.
    notes: Optional[str] = None
