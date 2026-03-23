import sys
import os

# Add backend to path
sys.path.append('/home/rehack/PycharmProjects/mrpfx-backend')

from app.schema.services import PropFirmRegisterRequest
from pydantic import ValidationError

def test_schema():
    print("Testing PropFirmRegisterRequest with relaxed values...")
    valid_data = {
        "login_id": "12345",
        "password": "password123",
        "propfirm_name": "FTMO",
        "propfirm_website_link": "N/A",  # Relaxed
        "server_name": "FTMO-Demo",
        "server_type": "Metatrader 5 only",  # Relaxed
        "challenges_step": 2,
        "propfirm_account_cost": 155.0,
        "account_size": 10000.0,
        "account_phases": 2,
        "trading_platform": "Metatrader 5 only",
        "propfirm_rules": "Relaxed rules",  # Relaxed
        "whatsapp_no": "+123456789",
        "telegram_username": "@testuser",
        "payment_method": "card"  # New field
    }

    try:
        req = PropFirmRegisterRequest(**valid_data)
        print("✅ Schema validation successful!")
        print(f"Payment Method: {req.payment_method}")
    except ValidationError as e:
        print("❌ Schema validation failed!")
        print(e)

if __name__ == "__main__":
    test_schema()
