import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.service.email import render_template
from app.core.config import settings

def test_render():
    templates = [
        ("email/crypto_payment_success.html", {"user_name": "Test User", "payment_id": "PAY-123", "status": "finished"}),
        ("email/admin_crypto_payment_received.html", {"user_email": "user@example.com", "payment_id": "PAY-123", "status": "finished"}),
        ("email/crypto_payment_partial.html", {"user_name": "Test User", "payment_id": "PAY-123", "status": "partially_paid"}),
        ("email/crypto_payment_failed.html", {"user_name": "Test User", "payment_id": "PAY-123", "status": "failed"}),
    ]

    for template_name, context in templates:
        try:
            content = render_template(template_name, **context)
            print(f"Successfully rendered {template_name}")
            # print(content[:100] + "...")
        except Exception as e:
            print(f"Error rendering {template_name}: {e}")

if __name__ == "__main__":
    test_render()
