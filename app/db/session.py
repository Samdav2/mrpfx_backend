from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

from app.core.config import settings


# SQLite doesn't support pool_size, so we handle it conditionally
if settings.USE_SQLITE:
    engine = create_async_engine(
        url=settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
        # SQLite needs this for proper async support
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_async_engine(
        url=settings.DATABASE_URL,
        max_overflow=10,
        future=True,
        pool_size=20,
        pool_pre_ping=True,  # Check connection liveness
        echo=settings.DEBUG,
    )


async def get_session() -> AsyncSession:
    """
    An asynchronous session factory that creates a new session
    """
    async with AsyncSession(engine) as session:
        yield session


async def ini_db():
    """
    A function that creates database tables from the models
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
