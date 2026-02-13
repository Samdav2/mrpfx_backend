import asyncio
from sqlalchemy import text
from app.db.session import engine

async def check_um_meta():
    async with engine.connect() as conn:
        try:
            result = await conn.execute(text('SELECT * FROM "8jH_um_metadata" LIMIT 20'))
            rows = result.all()
            print(f"Rows in 8jH_um_metadata: {len(rows)}")
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_um_meta())
