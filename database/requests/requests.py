from sqlalchemy import select, insert, delete
from database.session import AsyncSessionLocal
from database.models.models import User
from source.user import UserClass

async def add_user_if_not_exists(user_instance : UserClass):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_instance.user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            new_user = User(user_id=user_instance.user_id, username=user_instance.username)
            session.add(new_user)
            await session.commit()


async def is_admin(user_instance : UserClass) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_instance.user_id)
        )
        user = result.scalar_one_or_none()
        return user.is_admin
