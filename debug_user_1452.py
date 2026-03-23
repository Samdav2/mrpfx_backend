import asyncio
from sqlalchemy import text
from app.db.session import engine

async def check_user():
    print("Checking database for User 5 and constraints...")
    try:
        async with engine.begin() as conn:
            # Check if user 5 exists
            result = await conn.execute(text("SELECT ID, user_login FROM `8jH_users` WHERE ID = 5"))
            user = result.fetchone()
            if user:
                print(f"User 5 EXISTS: {user}")
            else:
                print("User 5 DOES NOT EXIST in 8jH_users table!")

            # Check table engine
            result = await conn.execute(text("SHOW TABLE STATUS LIKE '8jH_users'"))
            users_engine = result.fetchone()
            print(f"8jH_users Engine: {users_engine.Engine if users_engine else 'Unknown'}")

            result = await conn.execute(text("SHOW TABLE STATUS LIKE '8jH_copy_trading_connections'"))
            conn_engine = result.fetchone()
            print(f"8jH_copy_trading_connections Engine: {conn_engine.Engine if conn_engine else 'Unknown'}")

    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    asyncio.run(check_user())
