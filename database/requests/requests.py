from sqlalchemy import select, insert, delete, and_
from database.session import AsyncSessionLocal
from database.models.models import User
from source.user import UserClass
from database.models.models import UserEventConnect
from database.models.models import Event
from source.working_classes import Event as EventDTO
from datetime import datetime


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

async def add_event_if_not_exists(event_instance: EventDTO) -> Event:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_event = await session.execute(
                select(Event).where(Event.id == event_instance.id)
            )
            existing_event = existing_event.scalar_one_or_none()
            if existing_event is None:
                new_event = Event(
                    _title=event_instance.title,
                    _description=event_instance.description,
                    _start_time=event_instance.start_time,
                    _end_time=event_instance.end_time,
                    _link=event_instance.link,
                    _location=event_instance._location,
                    _status=event_instance._status,
                    _vacant_places=event_instance._vacant_places,
                    _activities=event_instance._activities,
                    _id=event_instance.id
                )
                session.add(new_event)
                await session.flush()
                return new_event
            return existing_event


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
                await session.flush()
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


