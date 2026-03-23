import requests

BASE_URL = "http://localhost:8000"
API_KEY = "bdbd0da428c30a13e7f8a9a11a259204b210847da7a8473dbeee62c65387c3bc"

def test_unprotected_health():
    print("Testing /health without API Key...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code} (Expected 403)")
    return response.status_code == 403

def test_protected_health():
    print("Testing /health with API Key...")
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    print(f"Status Code: {response.status_code} (Expected 200)")
    return response.status_code == 200

def test_traders_unauthenticated():
    print("Testing /api/v1/traders with API Key but no Token...")
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(f"{BASE_URL}/api/v1/traders", headers=headers)
    print(f"Status Code: {response.status_code} (Expected 401)")
    return response.status_code == 401

def test_login_no_api_key():
    print("Testing /api/v1/auth/login without API Key...")
    payload = {"login": "test", "password": "testpassword"}
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
    print(f"Status Code: {response.status_code} (Expected 403)")
    return response.status_code == 403

if __name__ == "__main__":
    results = [
        test_unprotected_health(),
        test_protected_health(),
        test_traders_unauthenticated(),
        test_login_no_api_key()
    ]

    if all(results):
        print("\n✅ All security verification tests passed!")
    else:
        print("\n❌ Some tests failed.")
