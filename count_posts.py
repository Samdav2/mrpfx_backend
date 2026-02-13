import asyncio
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def count_posts():
    async with AsyncSession(engine) as session:
        # Group by post_type
        print("Post Type counts:")
        stmt = select(WPPost.post_type, func.count(WPPost.ID)).group_by(WPPost.post_type)
        result = await session.exec(stmt)
        for ptype, count in result.all():
            print(f"- {ptype}: {count}")

if __name__ == "__main__":
    asyncio.run(count_posts())
