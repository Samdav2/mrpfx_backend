import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta

async def find_image_meta_keys():
    async with AsyncSession(engine) as session:
        stmt = select(WPPostMeta.meta_key).distinct()
        result = await session.exec(stmt)
        keys = result.all()

        print("Meta Keys containing image/thumb/media:")
        for key in keys:
            k_lower = key.lower()
            if "image" in k_lower or "thumb" in k_lower or "media" in k_lower or "attachment" in k_lower:
                print(f"- {key}")

if __name__ == "__main__":
    asyncio.run(find_image_meta_keys())
