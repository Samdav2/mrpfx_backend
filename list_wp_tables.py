import asyncio
from sqlalchemy import inspect
from app.db.session import wp_engine

async def list_wp_tables():
    async with wp_engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        print("Tables in WordPress DB:")
        for table in tables:
            print(f"- {table}")

if __name__ == "__main__":
    asyncio.run(list_wp_tables())
