import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta

async def find_url_meta():
    async with AsyncSession(engine) as session:
        stmt = select(WPPostMeta).where(WPPostMeta.meta_value.like("%http%"))
        result = await session.exec(stmt)
        metas = result.all()

        print("Meta entries containing URLs:")
        for m in metas:
            print(f"Post ID: {m.post_id}, Key: {m.meta_key}, Value: {m.meta_value}")

if __name__ == "__main__":
    asyncio.run(find_url_meta())
