import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.getcwd())

from app.service.email import render_template

def verify_templates():
    print("Verifying email templates...")

    # Verification Email
    try:
        html = render_template("email/verification.html", username="TestUser", code="123456")
        if "TestUser" in html and "123456" in html:
            print("Verification template: OK")
        else:
            print("Verification template: FAILED (Content mismatch)")
    except Exception as e:
        print(f"Verification template: FAILED ({e})")

    # Welcome Email
    try:
        html = render_template("email/welcome.html", username="TestUser", dashboard_url="http://localhost/dashboard")
        if "TestUser" in html and "http://localhost/dashboard" in html:
            print("Welcome template: OK")
        else:
            print("Welcome template: FAILED (Content mismatch)")
    except Exception as e:
        print(f"Welcome template: FAILED ({e})")

    # Reset Password Email
    try:
        html = render_template("email/reset_password.html", username="TestUser", reset_link="http://localhost/reset")
        if "TestUser" in html and "http://localhost/reset" in html:
            print("Reset Password template: OK")
        else:
            print("Reset Password template: FAILED (Content mismatch)")
    except Exception as e:
        print(f"Reset Password template: FAILED ({e})")

    # Order Confirmation Email
    try:
        html = render_template("email/order_confirmation.html", order_id=101, total=99.99, currency="USD", items=["Item 1", "Item 2"])
        if "101" in html and "99.99" in html and "Item 1" in html:
            print("Order Confirmation template: OK")
        else:
            print("Order Confirmation template: FAILED (Content mismatch)")
    except Exception as e:
        print(f"Order Confirmation template: FAILED ({e})")

    # Order Status Email
    try:
        html = render_template("email/order_status.html", order_id=101, new_status="completed")
        if "101" in html and "COMPLETED" in html:
            print("Order Status template: OK")
        else:
            print("Order Status template: FAILED (Content mismatch)")
    except Exception as e:
        print(f"Order Status template: FAILED ({e})")

if __name__ == "__main__":
    verify_templates()
