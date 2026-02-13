import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from sqlalchemy import inspect

async def check_columns():
    async with engine.connect() as conn:
        columns = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_columns("8jH_posts"))
        print("Columns in 8jH_posts:")
        for col in columns:
            print(f"- {col['name']} ({col['type']})")

if __name__ == "__main__":
    asyncio.run(check_columns())
