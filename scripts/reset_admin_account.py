import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, engine
from app.model.wordpress.core import WPUser
from app.core.security import hash_password

async def reset_admin():
    email = "Mrpfxworld@gmail.com"
    new_password = "@Gratitude556"

    async with AsyncSession(engine) as session:
        statement = select(WPUser).where(WPUser.user_email == email)
        results = await session.execute(statement)
        user = results.scalar_one_or_none()

        if not user:
            print(f"User {email} not found.")
            return

        print(f"Updating User: {user.user_login} (ID: {user.ID})")

        # Hash new password
        user.user_pass = hash_password(new_password)
        # Ensure admin status
        user.user_status = 1

        session.add(user)
        await session.commit()

        print(f"Successfully updated password and set user_status=1 for {email}")

if __name__ == "__main__":
    asyncio.run(reset_admin())
