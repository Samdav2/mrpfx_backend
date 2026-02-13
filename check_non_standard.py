import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta, WPPost

async def check_non_standard_image_meta():
    async with AsyncSession(engine) as session:
        # Look for _wp_attached_file on non-attachment posts
        stmt = select(WPPostMeta).where(WPPostMeta.meta_key == "_wp_attached_file")
        result = await session.exec(stmt)
        metas = result.all()

        print("Searching for _wp_attached_file on posts...")
        for m in metas:
            post = await session.get(WPPost, m.post_id)
            if post and post.post_type != "attachment":
                print(f"Found on ID {post.ID} ({post.post_type}): {m.meta_value}")

if __name__ == "__main__":
    asyncio.run(check_non_standard_image_meta())
