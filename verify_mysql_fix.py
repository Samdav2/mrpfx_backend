import asyncio
import os
import sys
from sqlalchemy import text

# Add project root to sys.path to import app modules correctly
sys.path.append(os.getcwd())

from app.db.session import engine
from app.core.config import settings

async def verify_mysql():
    print(f"DATABASE_URL: {settings.DATABASE_URL.split('@')[-1]}") # Hide credentials
    print(f"USE_SQLITE: {settings.USE_SQLITE}")

    try:
        async with engine.begin() as conn:
            # Check if we are really on MySQL
            result = await conn.execute(text("SELECT VERSION()"))
            version = result.scalar()
            print(f"Database Type/Version: {version}")

            # Check for User 5
            result = await conn.execute(text("SELECT ID, user_login FROM `8jH_users` WHERE ID = 5"))
            user = result.fetchone()
            if user:
                print(f"SUCCESS: User 5 exists in MySQL! {user}")
            else:
                print("WARNING: User 5 IS STILL MISSING in the MySQL database!")

                # Check for ANY users
                result = await conn.execute(text("SELECT COUNT(*) FROM `8jH_users`"))
                count = result.scalar()
                print(f"Total users in `8jH_users` table: {count}")

                if count > 0:
                    print("First 5 users in table:")
                    result = await conn.execute(text("SELECT ID, user_login FROM `8jH_users` LIMIT 5"))
                    for row in result.fetchall():
                        print(f" - ID: {row.ID}, Login: {row.user_login}")

    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_mysql())
