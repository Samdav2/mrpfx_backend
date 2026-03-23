import asyncio
from sqlmodel import SQLModel
from app.model.services import AccountManagementConnection, CopyTradingConnection, PropFirmRegistration
from app.db.session import engine
from app.model.wordpress.core import WPUser

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Created tables successfully")

if __name__ == "__main__":
    asyncio.run(create_tables())
