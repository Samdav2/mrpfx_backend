import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

# Import ALL models
print("--- Importing Models ---")
try:
    from app.model.crypto_payment import CryptoPayment
    from app.model.services import AccountManagementConnection, CopyTradingConnection, PropFirmRegistration
    from app.model.traders import Trader, TraderPerformance
    from app.model.user import User
    import app.model.wordpress as wp_models
    print(f"✓ {len(SQLModel.metadata.tables)} tables registered in metadata.")
except Exception as e:
    print(f"✗ Model Import Error: {e}")
    sys.exit(1)

async def init_db():
    print("\n--- Connecting to MySQL ---")
    url = settings.WP_DATABASE_URL
    print(f"URL: {url}")

    # Check if we have defaults or real values
    if "root" in url and "localhost" in url:
        print("WARNING: Using default 'root@localhost'. Check your .env if this is wrong.")

    engine = create_async_engine(url)

    try:
        async with engine.begin() as conn:
            # Test connection
            await conn.execute(wp_models.wp_core.text("SELECT 1"))
            print("✓ Connection successful.")

            # Create tables
            print("Creating tables (if missing)...")
            await conn.run_sync(SQLModel.metadata.create_all)
            print("✓ Tables created or verified.")

    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        print("\nPossible reasons:")
        print("1. Your .env file is NOT filled in (currently it looks like it has defaults)")
        print("2. Your database user doesn't have CREATE privileges")
        print("3. The password in .env is incorrect")
        sys.exit(1)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
