import asyncio
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select
from app.db.session import AsyncSession, engine
from app.model.wordpress.core import WPUserMeta

async def dump_meta():
    async with AsyncSession(engine) as session:
        statement = select(WPUserMeta).where(WPUserMeta.user_id == 9)
        results = await session.execute(statement)
        metas = results.scalars().all()

        print(f"\n--- USER META FOR ID 9 ---")
        for m in metas:
            print(f"Key: {m.meta_key:20} | Value: {m.meta_value}")

if __name__ == "__main__":
    asyncio.run(dump_meta())
