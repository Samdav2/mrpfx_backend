
import asyncio
from sqlmodel import select
from app.db.session import wp_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.wordpress.core import WPPost, WPPostMeta

async def check_dynamic_prices():
    print("Starting check_dynamic_prices...")
    async with AsyncSession(wp_engine) as session:
        print("Session opened.")
        for post_type in ["signal", "trading_tool", "forex_book"]:
            print(f"--- Checking {post_type} ---")
            stmt = select(WPPost).where(WPPost.post_type == post_type).limit(1)
            result = await session.exec(stmt)
            post = result.first()
            if post:
                print(f"ID: {post.ID}, Title: {post.post_title}")
                meta_stmt = select(WPPostMeta).where(WPPostMeta.post_id == post.ID)
                meta_result = await session.exec(meta_stmt)
                for meta in meta_result.all():
                    print(f"  {meta.meta_key}: {meta.meta_value}")
            else:
                print(f"No posts found for {post_type}")
    print("Done.")

if __name__ == "__main__":
    asyncio.run(check_dynamic_prices())
