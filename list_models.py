import os
import google.genai as genai

# Check API key is accessible
key = os.getenv("GOOGLE_API_KEY")
print("GOOGLE_API_KEY loaded?", bool(key))

# Create client
client = genai.Client(api_key=key)

print("\n=== AVAILABLE MODELS ===\n")
models = client.models.list()
for m in models:
    print(m.name)
