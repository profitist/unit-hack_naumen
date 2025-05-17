from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
import database.requests.requests as rq


async def admin_required(func):
    async def wrapper(message: Message):
        is_admin = rq.is_admin(message.from_user.id)
        if is_admin:
            await message.answer(text='Вы не являетесь организатором '
                                      'мероприятия!\n'
                                      'Вернитесь в главное меню!')
            return
        else:
            return await func(message)
    return await func
