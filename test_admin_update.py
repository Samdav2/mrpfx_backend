
import httpx
import asyncio
import json

async def test_admin_update():
    # Use registration ID 1 (FTMO-81781) for testing
    registration_id = 1
    url = f"http://localhost:8000/api/v1/admin/prop-firm/registrations/{registration_id}"

    payload = {
        "status": "failed", # Changed for testing
        "payment_status": "failed"
    }

    print(f"Connecting to: {url}")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print(f"--- Sending PATCH request ---")
            response = await client.patch(url, json=payload)
            print(f"Status Code: {response.status_code}")
            print("Response Payload:")
            print(json.dumps(response.json(), indent=2))

            # Verify the change
            print(f"\n--- Verifying update via GET /prop-firm/account/{registration_id} ---")
            response = await client.get(f"http://localhost:8000/api/v1/prop-firm/account/{registration_id}")
            data = response.json()
            print(f"Status: {data['data']['status']}")
            print(f"Payment Status: {data['data']['payment_status']}")

    except httpx.TimeoutException:
        print("Error: Request timed out. Is the server running and accessible?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_admin_update())
