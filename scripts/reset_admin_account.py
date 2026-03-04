import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, wp_engine
from app.model.wordpress.core import WPUser
from app.core.security import hash_password
from app.repo.wordpress.user import WPUserRepository

async def reset_admin():
    email = "Mrpfxworld@gmail.com"
    new_password = "@Gratitude556"

    async with AsyncSession(wp_engine) as session:
        user_repo = WPUserRepository(session)
        user = await user_repo.get_by_email(email)

        if not user:
            print(f"User {email} not found.")
            return

        print(f"Updating User: {user.user_login} (ID: {user.ID})")

        # Hash new password using WordPress-compatible hash (phpass)
        user.user_pass = hash_password(new_password)
        # In WordPress, user_status 0 is active.
        user.user_status = 0

        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Set the WordPress capabilities to administrator
        success = await user_repo.set_roles(user.ID, ["administrator"])

        if success:
            print(f"Successfully updated password and set administrator role for {email}")
        else:
            print(f"Updated password but failed to set administrator role for {email}")

if __name__ == "__main__":
    asyncio.run(reset_admin())
