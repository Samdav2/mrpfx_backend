import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.service.email import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
    send_order_confirmation_email,
    send_order_status_update_email,
    send_propfirm_login_success_email,
    send_course_enrollment_email,
    send_admin_new_user_email_notification,
    send_admin_new_order_notification
)
from app.core.config import settings

async def test_emails():
    # Target email from user request
    target_email = "adoxop1@gmail.com"
    app_name = "MRPFX"

    print(f"--- Starting Email Tests for {target_email} ---")

    # 1. Verification Email
    print("1. Sending Verification Email...")
    await send_verification_email(target_email, "123456", "TestUser")

    # 2. Password Reset Email
    print("2. Sending Password Reset Email...")
    await send_password_reset_email(target_email, "dummy-reset-token", "TestUser")

    # 3. Welcome Email
    print("3. Sending Welcome Email...")
    await send_welcome_email(target_email, "TestUser")

    # 4. Order Confirmation
    print("4. Sending Order Confirmation...")
    await send_order_confirmation_email(
        target_email,
        1001,
        99.99,
        "USD",
        ["MRPFX Starter Course", "Trading Strategy Guide"]
    )

    # 5. Order Status Update
    print("5. Sending Order Status Update...")
    await send_order_status_update_email(target_email, 1001, "completed")

    # 6. Prop Firm Login Success (Rebranded)
    print("6. Sending MRPFX Login Notification...")
    await send_propfirm_login_success_email(
        target_email,
        "TestUser",
        "LOG123456",
        "MetaTrader 5",
        f"{settings.FRONTEND_URL}/dashboard"
    )

    # 7. Course Enrollment
    print("7. Sending Course Enrollment...")
    await send_course_enrollment_email(
        target_email,
        "TestUser",
        "Advanced Forex Mastery",
        f"{settings.FRONTEND_URL}/courses/advanced-forex"
    )

    # 8. Admin New User Notification
    print("8. Sending Admin New User Notification...")
    await send_admin_new_user_email_notification(
        target_email, # Sending to target as admin for test
        "NewRegistrant",
        "newuser@example.com"
    )

    # 9. Admin New Order Notification
    print("9. Sending Admin New Order Notification...")
    await send_admin_new_order_notification(
        target_email, # Sending to target as admin for test
        2002,
        "John Doe",
        "johndoe@example.com",
        250.00,
        "USD",
        ["Prop Firm Challenge 100k"]
    )

    print("\n--- All Email Tests Triggered ---")
    print("Check adoxop1@gmail.com inbox (and spam folder).")

if __name__ == "__main__":
    asyncio.run(test_emails())
