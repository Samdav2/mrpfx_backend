import asyncio
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select, or_
from app.model.wordpress.core import WPUser as User
from datetime import datetime

DATABASE_URL = f"sqlite+aiosqlite:////{os.path.abspath('/home/rehack/PycharmProjects/mrpfx-backend/mrpfx.db')}"
engine = create_async_engine(DATABASE_URL)

async def test_update():
    print("Testing user_registered update...")
    async with AsyncSession(engine) as session:
        try:
            # 1. Get user
            stmt = select(User).where(User.ID == 10)
            result = await session.exec(stmt)
            user = result.first()
            if not user:
                print("User 10 not found")
                return

            print(f"Current registered: {user.user_registered}")

            # 2. Update password (like repository does)
            user.user_pass = "newpassword"
            await session.commit()
            await session.refresh(user)

            # 3. Update registered (like AuthService does)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Setting to: {now_str}")
            user.user_registered = now_str
            session.add(user)
            await session.commit()

            # 4. Verify
            await session.refresh(user)
            print(f"Verified registered: {user.user_registered}")

        except Exception as e:
            print(f"FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_update())
