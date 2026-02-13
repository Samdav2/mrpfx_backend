import asyncio
from sqlalchemy import text
from app.db.session import engine

async def find_image_options():
    async with engine.connect() as conn:
        try:
            # Note: 8jH_options starts with a digit, so it MUST be quoted in SQLite
            result = await conn.execute(text('SELECT option_name, option_value FROM "8jH_options" WHERE option_name LIKE \'%image%\' OR option_name LIKE \'%logo%\' OR option_name LIKE \'%thumb%\''))
            rows = result.all()
            print("Image-related options:")
            for name, value in rows:
                print(f"- {name}: {value[:200]}...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(find_image_options())
