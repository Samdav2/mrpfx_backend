import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def check_guids():
    async with AsyncSession(engine) as session:
        stmt = select(WPPost).where(WPPost.post_type.in_(["post", "page", "lp_course", "product"]))
        result = await session.exec(stmt)
        posts = result.all()

        print("Guids for common post types:")
        for post in posts:
            print(f"ID: {post.ID}, Type: {post.post_type}, Guid: {post.guid}")

if __name__ == "__main__":
    asyncio.run(check_guids())
