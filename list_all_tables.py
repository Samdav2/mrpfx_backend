import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from sqlalchemy import inspect

async def list_tables():
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        print("Tables in DB:")
        for table in tables:
            print(f"- {table}")

if __name__ == "__main__":
    asyncio.run(list_tables())
