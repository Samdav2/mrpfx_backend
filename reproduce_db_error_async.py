import asyncio
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select, or_
from app.model.wordpress.core import WPUser as User

DATABASE_URL = f"sqlite+aiosqlite:////{os.path.abspath('/home/rehack/PycharmProjects/mrpfx-backend/mrpfx.db')}"
engine = create_async_engine(DATABASE_URL)

async def reproduce():
    print("Testing with AsyncSession...")
    async with AsyncSession(engine) as session:
        try:
            stmt = select(User).limit(1)
            result = await session.exec(stmt)
            user = result.first()
            if user:
                print(f"Successfully retrieved user: {user.user_login}")
                print(f"Registered: [{user.user_registered}] ({type(user.user_registered)})")

                identifier = user.user_login
                stmt2 = select(User).where(or_(User.user_email == identifier, User.user_login == identifier))
                result2 = await session.exec(stmt2)
                user2 = result2.first()
                print(f"Retrieved by identifier {identifier}: {user2 is not None}")
            else:
                print("No users in database")
        except Exception as e:
            print(f"FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(reproduce())
