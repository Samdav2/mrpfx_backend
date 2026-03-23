import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from app.db.session import engine, wp_engine

# Import ALL models to ensure they are registered with SQLModel.metadata
print("Importing models...")
try:
    # Main app models
    from app.model.crypto_payment import CryptoPayment
    from app.model.services import AccountManagementConnection, CopyTradingConnection, PropFirmRegistration
    from app.model.traders import Trader, TraderPerformance
    from app.model.user import User as MainUser  # Avoid name clash

    # WordPress models (this imports all WP models from __init__.py)
    import app.model.wordpress as wp_models

    # Check what's registered
    tables = list(SQLModel.metadata.tables.keys())
    print(f"Total tables registered in metadata: {len(tables)}")
    print(f"Tabel names: {', '.join(tables[:10])}...")

    if len(tables) < 5:
        print("WARNING: Very few tables registered. Imports might not be working as expected.")

    print("All models imported successfully.")
except ImportError as e:
    print(f"Error importing models: {e}")
    sys.exit(1)

async def recreate_tables():
    """
    Create all missing tables in both the main and WordPress databases.
    Existing tables will NOT be dropped or modified.
    """
    print("\nStarting table creation process...")

    # 1. Main Application Database
    print(f"Checking main database: {engine.url.database}...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("✓ Main database tables verified/created.")
    except Exception as e:
        print(f"✗ Error creating main database tables: {e}")

    # 2. WordPress Database
    print(f"Checking WordPress database: {wp_engine.url.database}...")
    try:
        async with wp_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("✓ WordPress database tables verified/created.")
    except Exception as e:
        print(f"✗ Error creating WordPress database tables: {e}")

    print("\nDatabase initialization complete.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(recreate_tables())
