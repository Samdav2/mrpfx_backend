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

async def inspect_tables():
    url = get_env_db_url()
    engine = create_async_engine(url)

    try:
        async with engine.begin() as conn:
            print("--- 8jH_users definition ---")
            result = await conn.execute(text("SHOW CREATE TABLE `8jH_users`"))
            row = result.fetchone()
            print(row[1] if row else "Not found")

            print("\n--- 8jH_copy_trading_connections definition ---")
            result = await conn.execute(text("SHOW CREATE TABLE `8jH_copy_trading_connections`"))
            row = result.fetchone()
            print(row[1] if row else "Not found")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(inspect_tables())
