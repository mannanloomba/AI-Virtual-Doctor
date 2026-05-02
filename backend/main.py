# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

from backend.session_service import SessionService
from memory.memory_service import MemoryService

from agents.symptom_agent import SymptomAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.treatment_agent import TreatmentAgent
from agents.triage_agent import assess_triage
from agents.prescription_agent import PrescriptionAgent
from agents.vision_agent import VisionAgent

# NEW: ai agent wrapper
from backend.ai_agent import interpret_symptoms_with_llm, chat_with_doctor

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Virtual Doctor API - Final Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only; in prod, specify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize services and agents
session_service = SessionService()
memory_service = MemoryService()

symptom_agent = SymptomAgent(session_service=session_service)
diagnosis_agent = DiagnosisAgent()
treatment_agent = TreatmentAgent()
prescription_agent = PrescriptionAgent()
vision_agent = VisionAgent()

# Simple disclaimer for outputs
DISCLAIMER = ("This service is a clinical-assistance prototype for academic/competition use only. "
              "It is NOT a substitute for a licensed medical professional. For emergencies call local emergency services.")

@app.get("/")
def read_root():
    return {"message": "AI Virtual Doctor API is running. Visit /docs for the API documentation.", "status": "ok"}

@app.get("/health-check")
def health_check():
    return {"status": "ok", "disclaimer": DISCLAIMER}

@app.post("/symptom")
async def symptom_analysis(user_id: str = Form(...), text: str = Form(...)):
    out = await symptom_agent.parse_symptoms(user_id, text)
    triage = assess_triage(out["structured"])
    return {"structured": out, "triage": triage, "disclaimer": DISCLAIMER}

@app.post("/full-assess")
async def full_assess(user_id: str = Form(...), text: str = Form(...)):
    # 1) symptoms
    out = await symptom_agent.parse_symptoms(user_id, text)
    structured = out["structured"]

    # 2) diagnosis
    diag = await diagnosis_agent.diagnose(user_id=user_id, structured=structured)

    # 3) treatment
    treat = await treatment_agent.suggest(user_id=user_id, structured=structured, diagnosis=diag, patient_info={})

    # 4) prescription
    prescription = prescription_agent.create_prescription(user_id=user_id, treatment=treat)

    # 5) triage
    triage = assess_triage(structured)

    # 6) save to memory
    try:
        memory_service.add_medical_history(user_id, {"time": __import__("time").time(), "record": f"Auto-record: symptoms='{text}' -> diagnoses={ [d.get('id') for d in diag.get('probable_diagnoses', [])] }"})
    except Exception:
        pass

    return {
        "structured": out,
        "diagnosis": diag,
        "treatment": treat,
        "prescription": prescription,
        "triage": triage,
        "disclaimer": DISCLAIMER
    }

# NEW AI endpoints
@app.post("/ai-diagnosis")
async def ai_diagnosis(user_id: str = Form(...), text: str = Form(...)):
    out = await symptom_agent.parse_symptoms(user_id, text)
    structured = out["structured"]
    llm_result = interpret_symptoms_with_llm(user_id, structured)
    return {"structured": out, "llm": llm_result, "disclaimer": DISCLAIMER}

@app.post("/ai-treatment")
async def ai_treatment(user_id: str = Form(...), structured: str = Form(...)):
    # structured may be JSON string from frontend; keep flexible
    try:
        import json
        structured_obj = json.loads(structured) if isinstance(structured, str) else structured
    except Exception:
        structured_obj = structured
    llm_result = interpret_symptoms_with_llm(user_id, structured_obj)
    return {"treatment": llm_result.get("treatment_suggestion", []), "disclaimer": DISCLAIMER}

@app.post("/compare")
async def compare_modes(user_id: str = Form(...), text: str = Form(...)):
    # return rule-based and ai outputs for side-by-side comparison
    rule_out = await full_assess(user_id=user_id, text=text)
    ai_resp = await ai_diagnosis(user_id=user_id, text=text)
    return {"rule_based": rule_out, "ai_based": ai_resp}

@app.post("/chat")
async def chat(user_id: str = Form(...), message: str = Form(...), history: str = Form("[]")):
    import json
    try:
        hist = json.loads(history)
    except:
        hist = []
    
    response_text = chat_with_doctor(hist, message)
    return {"response": response_text}

@app.post("/upload-image")
async def upload_image(user_id: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    result = await vision_agent.analyze_image(user_id, content, file.filename)
    return JSONResponse(result)

@app.post("/user/add-history")
async def add_history(user_id: str = Form(...), record: str = Form(...)):
    memory_service.add_medical_history(user_id, {"time": __import__("time").time(), "record": record})
    return {"status": "success", "message": "History added", "added_record": record}

@app.get("/user/history")
async def get_history(user_id: str):
    return {"user_id": user_id, "history": memory_service.get_history(user_id)}
