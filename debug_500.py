from fastapi.testclient import TestClient
from app.main import app
import traceback

client = TestClient(app)

print("Starting diagnostic test...")
try:
    headers = {"X-API-KEY": "bdbd0da428c30a13e7f8a9a11a259204b210847da7a8473dbeee62c65387c3bc"}
    response = client.get("/health", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 500:
        print("Received 500 Internal Server Error.")
    else:
        print(f"Response Body: {response.text}")
except Exception:
    print("An exception occurred during the request:")
    traceback.print_exc()
