import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta

async def check_last_meta():
    async with AsyncSession(engine) as session:
        print("Last 30 meta entries:")
        stmt = select(WPPostMeta).order_by(WPPostMeta.meta_id.desc()).limit(30)
        res = await session.exec(stmt)
        for m in res.all():
            print(f"ID: {m.meta_id}, Post ID: {m.post_id}, Key: {m.meta_key}, Value: {m.meta_value}")

        print("\nAll thumbnail meta entries:")
        stmt2 = select(WPPostMeta).where(WPPostMeta.meta_key == "_thumbnail_id")
        res2 = await session.exec(stmt2)
        for m in res2.all():
            print(f"ID: {m.meta_id}, Post ID: {m.post_id}, Key: {m.meta_key}, Value: {m.meta_value}")

if __name__ == "__main__":
    asyncio.run(check_last_meta())
