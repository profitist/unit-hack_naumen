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
            new_user = User(user_id=user_instance.user_id, tg_id=user_instance.tg_id,
                            username=user_instance.username, first_name=user_instance.first_name,
                            last_name=user_instance.last_name, phone_number=user_instance.phone_number,
                            is_adimn=user_instance.is_admin)
            session.add(new_user)
            await session.commit()


async def is_admin(user_instance : UserClass) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_instance.user_id)
        )
        user = result.scalar_one_or_none()
        return user.is_admin
