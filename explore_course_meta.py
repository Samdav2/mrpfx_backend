import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta

async def explore_course_meta():
    async with AsyncSession(engine) as session:
        # Get all meta for ID 1 (School form - lp_course)
        print("Meta for Course ID 1:")
        stmt1 = select(WPPostMeta).where(WPPostMeta.post_id == 1)
        res1 = await session.exec(stmt1)
        for m in res1.all():
            print(f"  {m.meta_key}: {m.meta_value}")

if __name__ == "__main__":
    asyncio.run(explore_course_meta())
