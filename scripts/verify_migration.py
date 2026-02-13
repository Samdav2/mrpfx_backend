import asyncio
import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import engine
from app.model.user import User

async def verify_users():
    async with AsyncSession(engine) as session:
        stmt = select(User)
        result = await session.exec(stmt)
        users = result.all()

        print(f"Total users in DB: {len(users)}")
        for user in users:
            print(f"User: {user.user_login}, Email: {user.user_email}, Pass: {user.user_pass[:10]}...")

if __name__ == "__main__":
    asyncio.run(verify_users())
