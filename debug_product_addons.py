import asyncio
from sqlmodel import select
from app.db.session import engine
from app.model.wordpress.core import WPPostMeta
from sqlmodel.ext.asyncio.session import AsyncSession

async def main():
    product_id = 18618
    async with AsyncSession(engine) as session:
        stmt = select(WPPostMeta).where(WPPostMeta.post_id == product_id)
        result = await session.exec(stmt)
        for row in result:
            print(f"Key: {row.meta_key}, Val Preview: {row.meta_value[:100]}")

if __name__ == "__main__":
    asyncio.run(main())
