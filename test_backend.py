import requests
import json

url = "http://127.0.0.1:8000/full-assess"
data = {
    "user_id": "test_user",
    "text": "i have cold for last 6 days"
}

try:
    response = requests.post(url, data=data)
    print(response.status_code)
    with open("backend_response.json", "w") as f:
        json.dump(response.json(), f, indent=2)
except Exception as e:
    print(e)
