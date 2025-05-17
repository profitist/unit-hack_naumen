from sqlalchemy import select, insert, delete
from database.session import AsyncSessionLocal
from database.models.models import User


async def add_user_if_not_exists(user_id: int, username: str | None):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(user_id == User.user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            new_user = User(user_id=user_id, username=username)
            session.add(new_user)
            await session.commit()


async def is_admin(user_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(user_id == User.user_id)
        )
        pass