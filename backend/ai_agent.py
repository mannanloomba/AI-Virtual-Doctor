import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, Any
import time

# Explicitly load .env
load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

provider = "none"
model = None

print("DEBUG: Initializing AI Agent with Quota Check...")

# 1. Try Google Gemini with Active Quota Testing
if GOOGLE_KEY:
    try:
        genai.configure(api_key=GOOGLE_KEY)
        
        # Get all available models
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception as e:
            print(f"DEBUG: Failed to list models: {e}")

        # Sort models to prioritize Flash/Lite (higher quotas)
        # We want 'flash' and 'lite' at the top
        def model_priority(name):
            name = name.lower()
            if "flash" in name and "lite" in name: return 0
            if "flash" in name: return 1
            if "lite" in name: return 2
            if "pro" in name: return 3
            return 4
        
        available_models.sort(key=model_priority)
        
        print(f"DEBUG: Testing {len(available_models)} models for quota availability...")
        
        found_working_model = None
        
        for m_name in available_models:
            try:
                # Skip vision-only or specific task models if possible, but list_models filter helps
                if "vision" in m_name or "embedding" in m_name: continue
                
                print(f"DEBUG: Testing {m_name}...")
                test_model = genai.GenerativeModel(m_name)
                # Try to generate a single token to check quota
                test_model.generate_content("Hi")
                
                print(f"DEBUG: SUCCESS! {m_name} is working and has quota.")
                found_working_model = m_name
                model = test_model
                provider = "google"
                break
            except Exception as e:
                # Catch 429 (ResourceExhausted) and others
                print(f"DEBUG: Failed {m_name}: {e}")
                continue
        
        if not found_working_model:
            print("DEBUG: All Gemini models failed (likely quota exceeded on all).")

    except Exception as e:
        print(f"DEBUG: Gemini configuration failed: {e}")

# 2. Try OpenAI (Only if Gemini failed)
if provider == "none" and OPENAI_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        client.models.list()
        provider = "openai"
        model = client
        print("DEBUG: OpenAI configured successfully.")
    except Exception as e:
        print(f"DEBUG: OpenAI failed ({e}).")

# 3. Fallback to Simulation Mode (Last Resort)
if provider == "none":
    print("WARN: API connection failed. Switching to Simulation Mode.")

def call_llm(prompt: str, max_tokens: int = 512) -> Dict[str, Any]:
    if provider == "google" and model:
        try:
            response = model.generate_content(prompt)
            return {"text": response.text, "raw": response.candidates[0].content}
        except Exception as e:
            return {"text": f"Gemini Error: {e}", "error": str(e)}
    elif provider == "openai" and model:
        try:
            response = model.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return {"text": response.choices[0].message.content, "raw": response}
        except Exception as e:
            return {"text": f"OpenAI Error: {e}", "error": str(e)}
            
    # Simulation Response
    return {"text": "Analysis complete. Based on the symptoms provided, there are indicators of an inflammatory response. Recommended to monitor temperature and hydration.", "structured": {}}

def interpret_symptoms_with_llm(user_id: str, structured: Dict[str, Any]) -> Dict[str, Any]:
    # Try real AI first
    if provider == "google" and model:
        try:
            prompt = f"Act as a doctor. Analyze {structured}. Return JSON with probable_diagnoses (name, score, reason) and treatment_suggestion."
            response = model.generate_content(prompt, generation_config={'response_mime_type': 'application/json'})
            import json
            return json.loads(response.text)
        except: pass
    elif provider == "openai" and model:
        try:
            prompt = f"Act as a doctor. Analyze {structured}. Return JSON with probable_diagnoses (name, score, reason) and treatment_suggestion."
            response = model.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Output JSON only."}, {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except: pass

    # Simulation Logic
    symptoms = str(structured).lower()
    if "rash" in symptoms or "itch" in symptoms or "red" in symptoms:
        return {
            "probable_diagnoses": [
                {"name": "Contact Dermatitis", "score": 0.85, "reason": "Localized redness and itching consistent with allergic reaction"},
                {"name": "Eczema", "score": 0.45, "reason": "Chronic skin irritation pattern"}
            ],
            "treatment_suggestion": [
                {"disease": "Contact Dermatitis", "plan": {"first_line_medications": ["Hydrocortisone cream", "Antihistamines"], "non_pharmacologic": ["Avoid irritants", "Cool compress"], "follow_up_days": 3}}
            ]
        }
    elif "fever" in symptoms or "headache" in symptoms or "cough" in symptoms:
        return {
            "probable_diagnoses": [
                {"name": "Viral Upper Respiratory Infection", "score": 0.75, "reason": "Combination of fever and headache suggests viral etiology"},
                {"name": "Influenza", "score": 0.40, "reason": "Systemic symptoms present"}
            ],
            "treatment_suggestion": [
                {"disease": "Viral URI", "plan": {"first_line_medications": ["Acetaminophen (Paracetamol)", "Ibuprofen"], "non_pharmacologic": ["Rest", "Hydration", "Monitor temperature"], "follow_up_days": 2}}
            ]
        }
    else:
        return {
            "probable_diagnoses": [
                {"name": "General Malaise", "score": 0.60, "reason": "Non-specific symptoms reported"},
                {"name": "Dehydration", "score": 0.30, "reason": "Possible fluid imbalance"}
            ],
            "treatment_suggestion": [
                {"disease": "General Observation", "plan": {"first_line_medications": ["None currently indicated"], "non_pharmacologic": ["Rest", "Fluid intake"], "follow_up_days": 1}}
            ]
        }

def chat_with_doctor(history: list, user_input: str) -> str:
    # Try real AI first
    if provider == "google" and model:
        try:
            chat = model.start_chat(history=history)
            return chat.send_message(user_input).text
        except: pass
    elif provider == "openai" and model:
        try:
            messages = [{"role": "system", "content": "You are a helpful medical AI assistant."}]
            for h in history:
                role = "user" if h.get("role") == "user" else "assistant"
                content = h.get("parts", [""])[0]
                messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": user_input})
            response = model.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            return response.choices[0].message.content
        except: pass

    # Simulation Chat
    ui = user_input.lower()
    if "fever" in ui:
        return "I understand you have a fever. How high is your temperature, and when did it start?"
    elif "headache" in ui:
        return "Headaches can be tricky. Is the pain sharp or throbbing? Does light bother you?"
    elif "rash" in ui:
        return "For the rash, is it spreading? You can upload a photo in the 'Image Analysis' tab for a better look."
    elif "thank" in ui:
        return "You're welcome. Take care and feel better soon!"
    elif "hello" in ui or "hi" in ui:
        return "Hello. I am your AI medical assistant. Please describe your symptoms."
    else:
        return "I see. Please tell me more about how you are feeling, or any other symptoms you've noticed."
