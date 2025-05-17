from sqlalchemy import select, insert, delete, and_
from datetime import datetime
from database.session import AsyncSessionLocal
from database.models.models import User
from source.user import UserClass
from database.models.models import UserEventConnect
from database.models.models import Event
from source.working_classes import Event



async def add_user_if_not_exists(user_instance: UserClass):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(user_instance.user_id == User.user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            new_user = User(user_id=user_instance.user_id, tg_id=user_instance.tg_id,
                            username=user_instance.username, first_name=user_instance.first_name,
                            last_name=user_instance.last_name, phone_number=user_instance.phone_number,
                            is_admin=user_instance.is_admin)
            session.add(new_user)
            await session.commit()


async def add_user_if_not_exists(user_instance: UserClass) -> User:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Ищем пользователя по tg_id (уникальному полю)
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
                await session.flush()  # Получаем сгенерированный user_id
                return new_user
            return existing_user



async def show_all_events():
    async with AsyncSessionLocal() as session:
        current_datetime = datetime.now()
        result = await session.execute(
            select(Event)
            .where(Event.datetime >= current_datetime)
            .order_by(Event.datetime.asc())
        )
        events = result.scalars().all()
        return events if events else []


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


async def user_id_by_tg_id(tg_id):
    return True
# TO DO


