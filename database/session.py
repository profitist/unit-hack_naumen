from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)
from database.models.models import *
from dotenv import dotenv_values


DATABASE_URL = dotenv_values(".env").get("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
