import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, engine
from app.model.wordpress.core import WPUser

async def check():
    async with AsyncSession(engine) as session:
        user = (await session.execute(select(WPUser).where(WPUser.ID == 9))).scalar_one_or_none()
        if user:
            print(f"ID={user.ID}, Login={user.user_login}, Email={user.user_email}")
        else:
            print("User ID 9 not found")

if __name__ == "__main__":
    asyncio.run(check())
