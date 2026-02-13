import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def list_all_posts():
    async with AsyncSession(engine) as session:
        stmt = select(WPPost)
        result = await session.exec(stmt)
        posts = result.all()

        print(f"Total posts in 8jH_posts: {len(posts)}")
        for post in posts:
            print(f"ID: {post.ID}, Title: {post.post_title}, Type: {post.post_type}, Status: {post.post_status}")

if __name__ == "__main__":
    asyncio.run(list_all_posts())
