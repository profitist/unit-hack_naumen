from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from database.models.models import Base

DATABASE_URL = "postgresql+asyncpg://botuser:botpass@localhost:5432/botdb"

engine = create_async_engine(DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
