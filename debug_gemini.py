import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"Key prefix: {api_key[:5]}...")

    genai.configure(api_key=api_key)

    print("\nAttempting to list models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

    print("\nAttempting to generate content with 'gemini-pro'...")
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error with gemini-pro: {e}")

    print("\nAttempting to generate content with 'gemini-1.5-flash'...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error with gemini-1.5-flash: {e}")
