import requests

url = "http://127.0.0.1:8000/api/predict/"
data = {
    "latitude": 28.6139,
    "longitude": 77.2090
}

try:
    response = requests.post(url, json=data)
    print(response.json())
except Exception as e:
    print("Error:", e)