import asyncio
from sqlalchemy import inspect, text
from app.db.session import engine

async def check_yoast():
    async with engine.connect() as conn:
        columns = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_columns("8jH_yoast_indexable"))
        print("Columns in 8jH_yoast_indexable:")
        for col in columns:
            if "image" in col['name'].lower():
                print(f"- {col['name']} ({col['type']})")

        # Check some data
        result = await conn.execute(text('SELECT object_id, twitter_image, open_graph_image FROM "8jH_yoast_indexable" WHERE twitter_image IS NOT NULL OR open_graph_image IS NOT NULL LIMIT 5'))
        rows = result.all()
        print(f"\nYoast Image Data: {len(rows)} rows found.")
        for row in rows:
            print(row)

if __name__ == "__main__":
    asyncio.run(check_yoast())
