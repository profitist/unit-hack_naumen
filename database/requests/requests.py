from sqlalchemy import select, insert, delete
from database.session import AsyncSessionLocal
from database.models.models import User
from source.user import UserClass
from source.working_classes import Event


async def add_user_if_not_exists(user_instance: UserClass) -> User:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_user = await session.execute(
                select(User).where(User.tg_id == user_instance.tg_id)
            )
            existing_user = existing_user.scalar_one_or_none()

            if existing_user is None:
                new_user = User(
                    tg_id=user_instance.tg_id,
                    username=user_instance.username,
                    first_name=user_instance.first_name,
                    last_name=user_instance.last_name,
                    phone_number=user_instance.phone_number,
                    is_admin=user_instance.is_admin
                )
                session.add(new_user)
                await session.flush()
                return new_user
            return existing_user


async def is_admin(user_id: int) -> bool:
    print(user_id)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(user_id == User.tg_id)
        )
        user = result.scalar_one_or_none()
        print(user)
        if user is None:
            return False
        return user.is_admin


async def add_event(event: Event):
    pass