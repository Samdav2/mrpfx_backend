import asyncio
from sqlmodel import select
from app.db.session import engine
from app.model.wordpress.core import WPPost
from sqlmodel.ext.asyncio.session import AsyncSession

async def main():
    async with AsyncSession(engine) as session:
        stmt = select(WPPost.post_title).where(WPPost.post_type == "global_product_addon")
        result = await session.exec(stmt)
        rows = result.all()
        print(f"Found {len(rows)} global product addons.")
        for title in rows:
            print(f"- {title}")

if __name__ == "__main__":
    asyncio.run(main())
