import asyncio
from sqlalchemy import inspect
from app.db.session import engine

async def check_nextend_columns():
    async with engine.connect() as conn:
        columns = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_columns("8jH_nextend2_image_storage"))
        print("Columns in 8jH_nextend2_image_storage:")
        for col in columns:
            print(f"- {col['name']} ({col['type']})")

if __name__ == "__main__":
    asyncio.run(check_nextend_columns())
