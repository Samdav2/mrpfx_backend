import asyncio
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from app.model.wordpress.core import WPUser as User
from datetime import datetime

DATABASE_URL = f"sqlite+aiosqlite:////{os.path.abspath('/home/rehack/PycharmProjects/mrpfx-backend/mrpfx.db')}"
engine = create_async_engine(DATABASE_URL)

async def check_login_logic(user_id):
    print(f"Checking login logic for user {user_id}...")
    async with AsyncSession(engine) as session:
        # Get user
        stmt = select(User).where(User.ID == user_id)
        result = await session.exec(stmt)
        user = result.first()
        if not user:
            print("User not found")
            return

        # Get force reset date
        from app.repo.wordpress.options import WPOptionRepository
        option_repo = WPOptionRepository(session)
        force_reset_date_str = await option_repo.get_option("force_password_reset_date")
        force_reset_date = int(force_reset_date_str) if force_reset_date_str else 0

        # Get last pass reset meta
        from app.repo.wordpress.user import WPUserRepository
        wp_user_repo = WPUserRepository(session)
        last_reset_str = await wp_user_repo.get_last_password_reset(user.ID)
        last_reset_ts = int(last_reset_str) if last_reset_str else 0

        # Calculate reg_ts
        try:
            reg_dt = datetime.strptime(user.user_registered, "%Y-%m-%d %H:%M:%S")
            reg_ts = int(reg_dt.timestamp())
        except Exception as e:
            print(f"Parsing error: {e}")
            reg_ts = 0

        effective_reset_ts = max(last_reset_ts, reg_ts)

        print(f"User registered (str): {user.user_registered}")
        print(f"User registered (ts):  {reg_ts}")
        print(f"Last reset (meta ts):  {last_reset_ts}")
        print(f"Force reset date:      {force_reset_date}")
        print(f"Effective reset ts:    {effective_reset_ts}")

        if effective_reset_ts < force_reset_date:
            print("RESULT: PASSWORD_RESET_REQUIRED")
        else:
            print("RESULT: LOGIN ALLOWED")

if __name__ == "__main__":
    asyncio.run(check_login_logic(10))
