
import httpx
import asyncio
import json

async def test_registration():
    url = "http://localhost:8000/api/v1/prop-firm/register"
    payload = {
        "login_id": "123456",
        "password": "securepassword123",
        "propfirm_name": "Funding Pips",
        "propfirm_website_link": "https://fundingpips.com",
        "server_name": "FundingPips-Demo",
        "server_type": "Demo",
        "challenges_step": 1,
        "propfirm_account_cost": 100.0,
        "account_size": 10000.0,
        "account_phases": 2,
        "trading_platform": "Metatrader 5",
        "propfirm_rules": "Rule 1: No gambling. Rule 2: Minimum 5 trading days. Rule 3: Max drawdown 10%. Rule 4: Daily drawdown 5%. Rule 5: Profit target 10%. Rule 6: No news trading. Rule 7: No weekend holding. Rule 8: Use SL. Rule 9: Be consistent. Rule 10: Have fun.",
        "whatsapp_no": "+1234567890",
        "telegram_username": "john_doe"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            print(f"Status Code: {response.status_code}")
            print("Response Payload:")
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_registration())
