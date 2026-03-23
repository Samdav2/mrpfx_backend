import requests

BASE_URL = "http://localhost:8000"

def test_account_management():
    print("Testing Account Management Connect...")
    payload = {
        "accountId": "12345678",
        "password": "mysecretpassword123",
        "server": "server1",
        "capital": 600,
        "manager": "managerA",
        "agreed": True
    }

    response = requests.post(f"{BASE_URL}/api/v1/account-management/connect", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_account_management_invalid_capital():
    print("Testing Account Management Connect (Invalid Capital < 500)...")
    payload = {
        "accountId": "12345678",
        "password": "mysecretpassword123",
        "server": "server1",
        "capital": 400,
        "manager": "managerA",
        "agreed": True
    }

    response = requests.post(f"{BASE_URL}/api/v1/account-management/connect", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_copy_trading():
    print("Testing Copy Trading Connect...")
    payload = {
        "accountId": "87654321",
        "password": "anotherpassword456",
        "server": "server2"
    }

    response = requests.post(f"{BASE_URL}/api/v1/copy-trading/connect", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == "__main__":
    test_account_management()
    test_account_management_invalid_capital()
    test_copy_trading()
