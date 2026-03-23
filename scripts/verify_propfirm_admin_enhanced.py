
import httpx
import asyncio
import json

async def verify_enhanced_propfirm_admin():
    base_url = "http://localhost:8000/api/v1"

    print("\n--- Testing GET /admin/prop-firm/registrations ---")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{base_url}/admin/prop-firm/registrations")
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Count: {data.get('count')}")
                if data.get('data'):
                    first = data['data'][0]
                    print("First registration sample:")
                    print(f"  Order ID: {first.get('order_id')}")
                    print(f"  User Name: {first.get('user_name')}")
                    print(f"  User Email: {first.get('user_email')}")

                    reg_id = first.get('registration_id')

                    print(f"\n--- Testing PATCH /admin/prop-firm/registrations/{reg_id} ---")
                    # Toggle status between 'pending' and 'active' (or similar)
                    current_status = first.get('status')
                    new_status = "active" if current_status == "pending" else "pending"

                    payload = {"status": new_status}
                    patch_response = await client.patch(
                        f"{base_url}/admin/prop-firm/registrations/{reg_id}",
                        json=payload
                    )
                    print(f"Patch Status Code: {patch_response.status_code}")
                    if patch_response.status_code == 200:
                        patch_data = patch_response.json()
                        print(f"New Status: {patch_data['data'].get('status')}")
                        print("Check server logs for email task execution.")
                    else:
                        print(f"Patch Error: {patch_response.text}")
                else:
                    print("No registrations found to test update.")
            else:
                print(f"Error: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_enhanced_propfirm_admin())
