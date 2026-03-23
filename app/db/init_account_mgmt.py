import asyncio
from sqlmodel import SQLModel
from app.db.session import engine
from app.model.user import User
from app.model.traders import Trader, TraderPerformance
from app.model.services import AccountManagementConnection, CopyTradingConnection, PropFirmRegistration

async def init_db():
    print("Initializing database...")
    async with engine.begin() as conn:
        # Drop it first to be sure
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(init_db())
