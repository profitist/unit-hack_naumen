from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                                InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить новое событие")],
        [KeyboardButton(text="Актуальные события 🗓")]
    ],
    resize_keyboard=True
)

main_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зарегистрироваться ✔"), KeyboardButton(text="Актуальные события 🗓")],
        [KeyboardButton(text="Мой профиль"), KeyboardButton(text="О нас ℹ️"), KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True
)

profile_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мои мероприятия"), KeyboardButton(text="Мои очереди")],
        [KeyboardButton(text="Мои данные"), KeyboardButton(text="Изменить данные")]
    ],
    resize_keyboard=True
)



back_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

reply_test = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Акутуальные события 🗓")],
        [KeyboardButton(text="Помощь 🫂"), KeyboardButton(text="О нас ℹ️"), KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True
)

settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ХУЙЧИК', url='https://unit-ekb.ru/')]])

manus = ['Platonn228', 'IVANUS', 'STEPA', 'ZALUPA']


async def inline_manus():
    keyboard = InlineKeyboardBuilder()
    for man in manus:
        keyboard.add(InlineKeyboardButton(text=man, url='https://github.com/Platonn3'))
    return keyboard.adjust(1).as_markup()

