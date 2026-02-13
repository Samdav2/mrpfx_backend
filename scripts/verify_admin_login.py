import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.db.session import get_session
from app.service.auth import AuthService
from app.schema.auth import LoginRequest
from app.schema.user import UserCreate
from app.repo.user import UserRepository
from app.core.security import hash_password

async def verify_admin_login():
    print("Starting Admin Login Verification...")

    async for session in get_session():
        user_repo = UserRepository(session)
        auth_service = AuthService(session)

        # 1. Create a regular user (status 0)
        print("\n1. Creating regular user (status 0)...")
        regular_email = "regular_test@example.com"
        regular_pass = "password123"

        # Cleanup if exists
        existing = await user_repo.get_by_email(regular_email)
        if existing:
            await session.delete(existing)
            await session.commit()

        regular_user = await user_repo.create(UserCreate(
            user_login="regular_test",
            user_pass=hash_password(regular_pass),
            user_email=regular_email,
            user_status=0,
            user_nicename="regular-test",
            user_url="",
            user_activation_key=""
        ))
        print(f"Created regular user: {regular_user.user_email} (Status: {regular_user.user_status})")

        # 2. Create an admin user (status 1)
        print("\n2. Creating admin user (status 1)...")
        admin_email = "admin_test@example.com"
        admin_pass = "adminpass123"

        # Cleanup if exists
        existing_admin = await user_repo.get_by_email(admin_email)
        if existing_admin:
            await session.delete(existing_admin)
            await session.commit()

        admin_user = await user_repo.create(UserCreate(
            user_login="admin_test",
            user_pass=hash_password(admin_pass),
            user_email=admin_email,
            user_status=1,
            user_nicename="admin-test",
            user_url="",
            user_activation_key=""
        ))
        print(f"Created admin user: {admin_user.user_email} (Status: {admin_user.user_status})")

        # 3. Attempt admin login with regular user
        print("\n3. Attempting admin login with regular user...")
        try:
            await auth_service.admin_login(LoginRequest(login=regular_email, password=regular_pass))
            print("FAILED: Regular user was allowed to login as admin!")
        except Exception as e:
            if "403" in str(e) or "Access denied" in str(e):
                print("SUCCESS: Regular user denied access as expected.")
            else:
                print(f"FAILED: Unexpected error: {e}")

        # 4. Attempt admin login with admin user
        print("\n4. Attempting admin login with admin user...")
        try:
            token = await auth_service.admin_login(LoginRequest(login=admin_email, password=admin_pass))
            print("SUCCESS: Admin user logged in successfully.")
            print(f"Token received: {token.access_token[:20]}...")
        except Exception as e:
            print(f"FAILED: Admin user failed to login: {e}")

        # Cleanup
        print("\nCleaning up...")
        await session.delete(regular_user)
        await session.delete(admin_user)
        await session.commit()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(verify_admin_login())
