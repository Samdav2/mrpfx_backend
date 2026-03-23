
import httpx
import asyncio
import json

async def test_get_registrations():
    base_url = "http://localhost:8000/api/v1/prop-firm/registrations"

    try:
        async with httpx.AsyncClient() as client:
            # 1. Get all registrations
            print("--- Testing GET /registrations ---")
            response = await client.get(base_url)
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(json.dumps(data, indent=2))

            if data["success"] and data["count"] > 0:
                reg_id = data["data"][0]["registration_id"]

                # 2. Get specific registration
                print(f"\n--- Testing GET /registrations/{reg_id} ---")
                response = await client.get(f"{base_url}/{reg_id}")
                print(f"Status Code: {response.status_code}")
                print(json.dumps(response.json(), indent=2))
            else:
                print("No registrations found to test individual GET.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_get_registrations())
