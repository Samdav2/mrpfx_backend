import asyncio
from sqlalchemy import text
from app.db.session import engine

async def check_nextend_data():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT * FROM 8jH_nextend2_image_storage"))
        rows = result.all()
        print(f"Rows in 8jH_nextend2_image_storage: {len(rows)}")
        for row in rows:
            print(row)

if __name__ == "__main__":
    asyncio.run(check_nextend_data())
