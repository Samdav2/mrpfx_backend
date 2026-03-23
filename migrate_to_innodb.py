import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

def get_env_db_url():
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

async def run_migration():
    url = get_env_db_url()
    engine = create_async_engine(url)

    try:
        async with engine.begin() as conn:
            print("Converting 8jH_users to InnoDB...")
            await conn.execute(text("ALTER TABLE `8jH_users` ENGINE=InnoDB"))

            print("Converting 8jH_copy_trading_connections to utf8mb4...")
            await conn.execute(text("ALTER TABLE `8jH_copy_trading_connections` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci"))

            print("SUCCESS: Database tables synchronized!")

    except Exception as e:
        print(f"Migration Failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_migration())
