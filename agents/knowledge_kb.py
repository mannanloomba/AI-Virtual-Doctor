# agents/knowledge_kb.py

KB = [
    {
        "id": "viral_upper_respiratory",
        "name": "Viral upper respiratory infection",
        "keywords": ["cough", "sore throat", "runny nose", "body pain", "fever", "cold", "headache"],
        "tests": ["None routine; consider rapid influenza or COVID test if indicated"],
        "treatment": {
            "non_pharmacologic": ["rest", "hydration", "saline gargles"],
            "medications": ["paracetamol/acetaminophen for fever and pain"],
            "follow_up_days": 5
        }
    },
    {
        "id": "cellulitis",
        "name": "Cellulitis",
        "keywords": ["swelling", "red", "reddish", "warm", "leg", "localized"],
        "tests": ["CBC", "blood culture", "wound swab if open wound"],
        "treatment": {
            "non_pharmacologic": ["elevation", "warm compresses"],
            "medications": ["oral antibiotics (e.g., cephalexin)"],
            "follow_up_days": 2
        }
    },
    {
        "id": "dengue",
        "name": "Dengue",
        "keywords": ["fever", "body pain", "retro-orbital pain", "rash"],
        "tests": ["Dengue NS1 / IgM, CBC (platelets)"],
        "treatment": {
            "non_pharmacologic": ["rest", "fluid replacement"],
            "medications": ["paracetamol only (avoid NSAIDs)"],
            "follow_up_days": 7
        }
    },
    {
        "id": "malaria",
        "name": "Malaria",
        "keywords": ["fever", "chills", "sweating", "recent travel"],
        "tests": ["Peripheral smear / rapid malaria antigen test", "CBC"],
        "treatment": {
            "non_pharmacologic": ["rest", "hydration"],
            "medications": ["antimalarials when confirmed"],
            "follow_up_days": 7
        }
    },
    {
        "id": "gastroenteritis",
        "name": "Gastroenteritis",
        "keywords": ["vomit", "vomiting", "diarrhea", "stomach", "abdomen", "after eating"],
        "tests": ["Stool test if severe", "electrolytes if dehydrated"],
        "treatment": {
            "non_pharmacologic": ["ORS / rehydration", "BRAT diet"],
            "medications": ["antiemetics if severe", "rehydration"],
            "follow_up_days": 3
        }
    }
]
