from sqlalchemy import select, insert, delete, and_
from database.session import AsyncSessionLocal
from database.models.models import *
from database.models.models import User, UserMasterclassConnect, MasterClass, MasterClassWaitingList, EventWaitingList
from source.user import UserClass
from database.models.models import UserEventConnect
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
                    user_id=user_instance.tg_id,
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


async def is_registered(user_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_user = await session.execute(
                select(User).where(User.tg_id == user_id)
            )
            existing_user = existing_user.scalar_one_or_none()
            if existing_user is None:
                return False
            return True


async def get_all_master_classes(event_id: int) -> list[MasterClass]:
    async with AsyncSessionLocal() as session:  # Добавлены скобки ()
        result = await session.execute(
            select(MasterClass)
            .where(MasterClass.event_id == event_id)
            .order_by(MasterClass.datetime.asc())  # Сортировка по дате
        )
        return result.scalars().all()  # Используем scalars().all() для списка



async def add_user_on_event(user_id: int, event_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                event = await session.execute(
                    select(Event)
                    .where(
                        and_(
                            Event.id == event_id,
                            Event.datetime >= datetime.now(),
                            Event.vacant_places > 0
                        )
                    )
                )
                event = event.scalar_one_or_none()

                if event is None:
                    return False
                existing_reg = await session.execute(
                    select(UserEventConnect)
                    .where(
                        and_(
                            UserEventConnect.user_id == user_id,
                            UserEventConnect.event_id == event_id
                        )
                    )
                )

                if existing_reg.scalar_one_or_none() is not None:
                    return False
                new_reg = UserEventConnect(
                    user_id=user_id,
                    event_id=event_id,
                    date_of_registration=datetime.now()
                )
                session.add(new_reg)
                event.vacant_places -= 1

                await session.commit()
                return True

            except Exception as e:
                await session.rollback()
                print(f"Error registering user: {e}")
                return False


async def add_user_on_master_class(user_id: int, master_class_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                master_class = await session.execute(
                    select(MasterClass)
                    .where(
                        and_(
                            MasterClass.id == master_class_id,
                            MasterClass.datetime >= datetime.now(),
                            MasterClass.vacant_places > 0
                        )
                    )
                )
                master_class = master_class.scalar_one_or_none()

                if master_class is None:
                    return False

                event_reg = await session.execute(
                    select(UserEventConnect)
                    .where(
                        and_(
                            UserEventConnect.user_id == user_id,
                            UserEventConnect.event_id == master_class.event_id
                        )
                    )
                )

                if event_reg.scalar_one_or_none() is None:
                    return False

                existing_reg = await session.execute(
                    select(UserMasterclassConnect)
                    .where(
                        and_(
                            UserMasterclassConnect.user_id == user_id,
                            UserMasterclassConnect.master_class_id == master_class_id
                        )
                    )
                )

                if existing_reg.scalar_one_or_none() is not None:
                    return False
                new_reg = UserMasterclassConnect(
                    user_id=user_id,
                    master_class_id=master_class_id,
                    date_of_registration=datetime.now()
                )
                session.add(new_reg)

                master_class.vacant_places -= 1

                await session.commit()
                return True

            except Exception as e:
                await session.rollback()
                print(f"Error registering for master class: {e}")
                return False


async def add_to_event_waiting_list(user_id: int, event_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_reg = await session.execute(
                select(UserEventConnect)
                .where(
                    and_(
                        UserEventConnect.user_id == user_id,
                        UserEventConnect.event_id == event_id
                    )
                )
            )
            if existing_reg.scalar_one_or_none() is not None:
                return False
            existing_wait = await session.execute(
                select(EventWaitingList)
                .where(
                    and_(
                        EventWaitingList.user_id == user_id,
                        EventWaitingList.event_id == event_id
                    )
                )
            )
            if existing_wait.scalar_one_or_none() is not None:
                return False
            new_wait = EventWaitingList(
                user_id=user_id,
                event_id=event_id,
                date_of_registration=datetime.now()
            )
            session.add(new_wait)
            await session.commit()
            return True


async def add_to_masterclass_waiting_list(user_id: int, master_class_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_reg = await session.execute(
                select(UserMasterclassConnect)
                .where(
                    and_(
                        UserMasterclassConnect.user_id == user_id,
                        UserMasterclassConnect.master_class_id == master_class_id
                    )
                )
            )
            if existing_reg.scalar_one_or_none() is not None:
                return False
            existing_wait = await session.execute(
                select(MasterClassWaitingList)
                .where(
                    and_(
                        MasterClassWaitingList.user_id == user_id,
                        MasterClassWaitingList.master_class_id == master_class_id
                    )
                )
            )
            if existing_wait.scalar_one_or_none() is not None:
                return False
            new_wait = MasterClassWaitingList(
                user_id=user_id,
                master_class_id=master_class_id,
                date_of_registration=datetime.now()
            )
            session.add(new_wait)
            await session.commit()
            return True


async def get_event_waiting_list(event_id: int) -> list[User]:
    """
    Возвращает список пользователей в листе ожидания мероприятия
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)
            .join(EventWaitingList, User.user_id == EventWaitingList.user_id)
            .where(EventWaitingList.event_id == event_id)
            .order_by(EventWaitingList.date_of_registration.asc())
        )
        return result.scalars().all()


async def get_masterclass_waiting_list(master_class_id: int) -> list[User]:
    """
    Возвращает список пользователей в листе ожидания мастер-класса
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)
            .join(MasterClassWaitingList, User.user_id == MasterClassWaitingList.user_id)
            .where(MasterClassWaitingList.master_class_id == master_class_id)
            .order_by(MasterClassWaitingList.date_of_registration.asc())
        )
        return result.scalars().all()


async def promote_from_waiting_list(event_id: int, count: int = 1) -> int:
    """
    Переводит первых N пользователей из листа ожидания в зарегистрированные
    Возвращает количество успешно переведенных пользователей
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Получаем мероприятие
            event = await session.execute(
                select(Event).where(Event.id == event_id)
            )
            event = event.scalar_one_or_none()

            if event is None or event.vacant_places < 1:
                return 0

            # Получаем первых N пользователей из листа ожидания
            waiting_users = await session.execute(
                select(EventWaitingList)
                .where(EventWaitingList.event_id == event_id)
                .order_by(EventWaitingList.date_of_registration.asc())
                .limit(min(count, event.vacant_places))
            )
            waiting_users = waiting_users.scalars().all()

            promoted = 0
            for wait in waiting_users:
                # Проверяем, не зарегистрирован ли уже
                existing_reg = await session.execute(
                    select(UserEventConnect)
                    .where(
                        and_(
                            UserEventConnect.user_id == wait.user_id,
                            UserEventConnect.event_id == event_id
                        )
                    )
                )
                if existing_reg.scalar_one_or_none() is None:
                    # Регистрируем
                    new_reg = UserEventConnect(
                        user_id=wait.user_id,
                        event_id=event_id,
                        date_of_registration=datetime.now()
                    )
                    session.add(new_reg)
                    event.vacant_places -= 1
                    promoted += 1

                    # Удаляем из листа ожидания
                    await session.delete(wait)

            await session.commit()
            return promoted


async def add_event_if_not_exists(event_instance: EventDTO) -> Event:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_event = await session.execute(
                select(Event).where(Event.id == event_instance.id)
            )
            existing_event = existing_event.scalar_one_or_none()
            if existing_event is None:
                new_event = Event(
                    title=event_instance.title,
                    description=event_instance.description,
                    datetime=event_instance.start_time,
                    vacant_places=event_instance._vacant_places,
                    address=event_instance._location
                )
                session.add(new_event)
                await session.flush()
                return new_event
            return existing_event


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


async def find_event(event_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Event)
            .where(Event.id == event_id)
        )
        event = result.scalar_one_or_none()
        return event


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


async def user_id_by_tg_id(tg_id: int) -> int | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.user_id)
            .where(User.tg_id == tg_id)
        )
        user_id = result.scalar_one_or_none()
        return user_id


async def get_all_tg_ids() -> list[int]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.tg_id))
        tg_ids = result.scalars().all()
        return tg_ids


async def show_all_events_of_user(user_instance: UserClass):
    async with AsyncSessionLocal() as session:
        current_datetime = datetime.now()

        # Получаем все мероприятия пользователя через связующую таблицу
        result = await session.execute(
            select(Event)
            .join(UserEventConnect, Event.id == UserEventConnect.event_id)
            .where(
                and_(
                    UserEventConnect.user_id == user_instance.user_id,
                    Event.datetime >= current_datetime  # Только будущие события
                )
            )
            .order_by(Event.datetime.asc())  # Сортировка по дате
        )

        return result.scalars().all()


async def get_faq():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(FAQ))
            faq_items = result.scalars().all()
            return faq_items


async def add_faq(question: str, answer: str) -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                insert(FAQ).values(question=question, answer=answer)
            )