from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
import database.requests.requests as rq


def admin_required(func):
    async def wrapper(message: Message, *args, **kwargs):
        is_admin = await rq.is_admin(message.from_user.id)
        if not is_admin:
            await message.answer(text='Вы не являетесь организатором '
                                      'мероприятия!\n'
                                      'Вернитесь в главное меню!')
            return
        else:
            return await func(message)
    return wrapper
