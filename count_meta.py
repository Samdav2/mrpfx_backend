import asyncio
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta

async def count_meta():
    async with AsyncSession(engine) as session:
        stmt = select(func.count(WPPostMeta.meta_id))
        result = await session.exec(stmt)
        count = result.one()
        print(f"Total rows in 8jH_postmeta: {count}")

        # also print first 50 rows to see what's in there
        stmt2 = select(WPPostMeta).limit(50)
        res2 = await session.exec(stmt2)
        print("\nFirst 50 meta entries:")
        for m in res2.all():
            print(f"ID: {m.meta_id}, Post ID: {m.post_id}, Key: {m.meta_key}, Value: {m.meta_value}")

if __name__ == "__main__":
    asyncio.run(count_meta())
