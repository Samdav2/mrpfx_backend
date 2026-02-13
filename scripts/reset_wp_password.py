import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, engine
from app.model.wordpress.core import WPUser
from app.core.security import hash_password, verify_password

async def reset_user_password(email: str, new_password: str):
    async with AsyncSession(engine) as session:
        # 1. Find the user
        statement = select(WPUser).where(WPUser.user_email == email)
        results = await session.execute(statement)
        user = results.scalar_one_or_none()

        if not user:
            print(f"USER NOT FOUND: {email}")
            return

        print(f"USER FOUND: ID={user.ID}, Login={user.user_login}, Email={user.user_email}")
        print(f"Old Hash: {user.user_pass}")

        # 2. Hash the new password with WordPress style (phpass)
        new_hash = hash_password(new_password)
        print(f"New WordPress-style Hash: {new_hash}")

        # 3. Update the user
        user.user_pass = new_hash
        session.add(user)
        await session.commit()
        print("\nDATABASE UPDATED SUCCESSFULLY!")

        # 4. Final verification check
        is_valid = verify_password(new_password, new_hash)
        print(f"Verification of new password: {'SUCCESS' if is_valid else 'FAILED'}")

if __name__ == "__main__":
    email = "Mrpfxworld@gmail.com"
    password = "@Gratitude55"

    asyncio.run(reset_user_password(email, password))
