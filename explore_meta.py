import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta

async def explore_meta():
    async with AsyncSession(engine) as session:
        # Get all meta keys to see if there's anything else image related
        stmt = select(WPPostMeta.meta_key).distinct()
        result = await session.exec(stmt)
        keys = result.all()

        print("Existing Meta Keys:")
        for key in keys:
            print(f"- {key}")

        # Get all meta for ID 41 (which the user might expect an image for)
        print("\nMeta for ID 41:")
        stmt41 = select(WPPostMeta).where(WPPostMeta.post_id == 41)
        res41 = await session.exec(stmt41)
        for m in res41.all():
            print(f"  {m.meta_key}: {m.meta_value}")

if __name__ == "__main__":
    asyncio.run(explore_meta())
