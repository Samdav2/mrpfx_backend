import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def check_content():
    async with AsyncSession(engine) as session:
        for pid in [44, 41]:
            post = await session.get(WPPost, pid)
            if post:
                print(f"ID: {post.ID}, Title: {post.post_title}")
                print(f"  Content: {post.post_content[:500]}...")

if __name__ == "__main__":
    asyncio.run(check_content())
