import asyncio
from sqlalchemy import text
from app.db.session import wp_engine

async def check():
    async with wp_engine.connect() as conn:
        for table in ["8jH_comments", "8jH_woocommerce_sessions", "8jH_users", "8jH_usermeta", "8jH_wc_customer_lookup"]:
            try:
                res = await conn.execute(text(f"SHOW CREATE TABLE {table}"))
                row = res.fetchone()
                if row:
                    print(f"--- {table} ---")
                    print(row[1])
            except Exception as e:
                print(f"Error checking {table}: {e}")

if __name__ == "__main__":
    asyncio.run(check())
