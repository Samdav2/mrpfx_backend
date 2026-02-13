import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPUserMeta

async def check_user_meta():
    async with AsyncSession(engine) as session:
        # Look for any image related keys in user meta
        stmt = select(WPUserMeta.meta_key).distinct()
        result = await session.exec(stmt)
        keys = result.all()

        print("User Meta Keys:")
        for key in keys:
            if any(x in key.lower() for x in ["image", "avatar", "thumb", "photo"]):
                print(f"- {key}")
            else:
                print(f"  (other): {key}")

if __name__ == "__main__":
    asyncio.run(check_user_meta())
