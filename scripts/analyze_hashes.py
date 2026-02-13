import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, engine
from app.model.wordpress.core import WPUser

async def analyze_hashes():
    async with AsyncSession(engine) as session:
        statement = select(WPUser)
        results = await session.execute(statement)
        users = results.scalars().all()
        print(f"\n--- USER HASH ANALYSIS (Total: {len(users)}) ---")
        for u in users:
            h = u.user_pass
            print(f"ID={u.ID:2} | Login={u.user_login:20} | Len={len(h):3} | Hash={h}")

if __name__ == "__main__":
    asyncio.run(analyze_hashes())
