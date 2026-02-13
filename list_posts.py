import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def list_posts():
    async with AsyncSession(engine) as session:
        stmt = select(WPPost).where(WPPost.post_type.in_(["post", "page", "lp_course", "product"]))
        result = await session.exec(stmt)
        posts = result.all()

        print(f"Listing {len(posts)} content items:")
        for post in posts:
            print(f"ID: {post.ID}, Title: {post.post_title}, Type: {post.post_type}, Status: {post.post_status}")

if __name__ == "__main__":
    asyncio.run(list_posts())
