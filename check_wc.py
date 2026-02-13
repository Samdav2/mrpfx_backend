import asyncio
from sqlalchemy import inspect
from app.db.session import engine

async def check_wc_columns():
    async with engine.connect() as conn:
        columns = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_columns("8jH_wc_product_meta_lookup"))
        print("Columns in 8jH_wc_product_meta_lookup:")
        for col in columns:
            print(f"- {col['name']} ({col['type']})")

if __name__ == "__main__":
    asyncio.run(check_wc_columns())
