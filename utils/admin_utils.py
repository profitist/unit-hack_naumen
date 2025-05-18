from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
import database.requests.requests as rq
import app.keyboards.admin_keyboards as ak
from functools import wraps


def admin_required(func):
    async def wrapper(message: Message, *args, **kwargs):
        allowed_kwargs = {}
        if "state" in kwargs:  # если нужен state
            allowed_kwargs["state"] = kwargs["state"]

        is_admin = await rq.is_admin(message.from_user.id)
        if not is_admin:
            await message.answer(
                text='Вы не являетесь организатором мероприятия!\n'
                     'Вернитесь в главное меню!')
            return
        return await func(message, *args, **allowed_kwargs)

    return wrapper


def reg_required(func):
    async def wrapper(message: Message, *args, **kwargs):
        founded_user = await rq.is_registered(message.from_user.id)
        if founded_user is None:
            await message.answer('Вы не зарегестрированы в системе, пожалуйста'
                                 'пройдите региистрацию!', ak.admin_menu)
            return
        return await func(message, *args, **kwargs)
    return wrapper


def reg_required_callback(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, **data):
        from_user = callback.from_user
        user_id = from_user.id

        # Проверка регистрации
        founded_user = await rq.is_registered(user_id)
        if founded_user is None:
            await callback.message.answer(
                'Вы не зарегистрированы в системе, пожалуйста пройдите регистрацию!',
                reply_markup=ak.admin_menu
            )
            return

        # Передаём всё, как есть, включая callback, FSM-состояние и всё остальное
        return await func(callback, **data)

    return wrapper
