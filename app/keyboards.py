from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                                InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Зарегистрироваться', callback_data='registration')]
])

main_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зарегистрироваться ✔"), KeyboardButton(text="Актуальные события 🗓")],
        [KeyboardButton(text="Помощь 🫂"), KeyboardButton(text="О нас ℹ️"), KeyboardButton(text="Задать вопрос")],
        [KeyboardButton(text="Назад")]
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

