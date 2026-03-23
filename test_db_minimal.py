import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine
from app.model.wordpress.core import WPPost

async def test_db():
    print("Starting minimal DB test...", flush=True)
    try:
        async with AsyncSession(engine) as session:
            print("Session created.", flush=True)
            stmt = select(WPPost).limit(1)
            print("Executing statement...", flush=True)
            result = await session.exec(stmt)
            print("Statement executed.", flush=True)
            post = result.first()
            print(f"Post found: {post.ID if post else 'None'}", flush=True)
        print("Test finished.", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test_db())
