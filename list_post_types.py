import asyncio
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def list_post_types():
    async with AsyncSession(engine) as session:
        stmt = select(WPPost.post_type).distinct()
        result = await session.exec(stmt)
        post_types = result.all()

        print("Unique Post Types:")
        for pt in post_types:
            print(f"- {pt}")

if __name__ == "__main__":
    asyncio.run(list_post_types())
