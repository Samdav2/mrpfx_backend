import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

def get_env_db_url():
    # Manual parsing of .env since Pydantic might be failing in some shell environments
    env_vars = {}
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    env_vars[k] = v.strip("'").strip('"')

    user = env_vars.get("DB_USER", "root")
    pw = env_vars.get("DB_PASSWORD", "")
    host = env_vars.get("DB_HOST", "localhost")
    port = env_vars.get("DB_PORT", "3306")
    name = env_vars.get("DB_NAME", "wordpress")

    return f"mysql+aiomysql://{user}:{pw}@{host}:{port}/{name}?charset=utf8mb4"

async def check_mysql_directly():
    url = get_env_db_url()
    print(f"Directly connecting to: {url.split('@')[-1]}")

    engine = create_async_engine(url)

    try:
        async with engine.begin() as conn:
            # Check user 5
            result = await conn.execute(text("SELECT ID, user_login FROM `8jH_users` WHERE ID = 5"))
            user = result.fetchone()
            if user:
                print(f"FOUND: User 5 exists! ({user.user_login})")
            else:
                print("MISSING: User 5 does NOT exist in the 8jH_users table in MySQL.")

                # Show first 5 users to see what's there
                result = await conn.execute(text("SELECT ID, user_login FROM `8jH_users` LIMIT 5"))
                print("Existing IDs in table:")
                for row in result:
                    print(f" - ID: {row.ID}, Login: {row.user_login}")

    except Exception as e:
        print(f"Connection Failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_mysql_directly())
