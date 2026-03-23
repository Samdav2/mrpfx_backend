import asyncio
from sqlmodel import select
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta
from sqlmodel.ext.asyncio.session import AsyncSession

async def main():
    async with AsyncSession(engine) as session:
        stmt = select(WPPostMeta).where(WPPostMeta.meta_key.like('%addon%'))
        result = await session.exec(stmt)
        rows = result.all()
        print(f"Found {len(rows)} matching addon meta keys.")
        for row in rows[:20]:
            print(f"Product ID: {row.post_id}, Key: {row.meta_key}, Val Preview: {row.meta_value[:150]}")

if __name__ == "__main__":
    asyncio.run(main())
