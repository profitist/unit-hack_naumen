from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                                InlineKeyboardMarkup, InlineKeyboardButton)
import database.requests.requests as rq

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
        [KeyboardButton(text="Мой профиль"), KeyboardButton(text="О нас ℹ️"), KeyboardButton(text="Задать вопрос")],
        [KeyboardButton(text='FAQ 🧐')]
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


reg_back_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_in_reg")]
    ]
)


reply_test = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Акутуальные события 🗓")],
        [KeyboardButton(text="Помощь 🫂"), KeyboardButton(text="О нас ℹ️"), KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True
)


async def inline_event_description(user_id: int, event_id: int):
    events = await rq.show_all_events_of_user(user_id)
    keyboard = InlineKeyboardBuilder()
    for event in events:
        if event.id == event_id:
            keyboard.add(InlineKeyboardButton(text='Мастерклассы', callback_data=f'master_classes_of_{event_id}'))
            return keyboard.adjust(1).as_markup()

    keyboard.add(InlineKeyboardButton(text='Зарегистрироваться', callback_data=f'reg_on_event_{event_id}'))
    keyboard.add(InlineKeyboardButton(text='Мастерклассы', callback_data=f'master_classes_of_{event_id}'))
    return keyboard.adjust(1).as_markup()


async def inline_masterclass_description(user_id: int, masterclass_id: int):
    masterclasses = await rq.show_all_master_classes_of_user(user_id)
    keyboard = InlineKeyboardBuilder()
    for masterclass in masterclasses:
        if masterclass_id == masterclass.id:
            return keyboard.as_markup()
    keyboard.add(InlineKeyboardButton(text='Зарегистрироваться', callback_data=f'reg_on_masterclass_{masterclass_id}'))
    return keyboard.adjust(1).as_markup()


settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ХУЙЧИК', url='https://unit-ekb.ru/')]])

manus = ['Platonn228', 'IVANUS', 'STEPA', 'ZALUPA']


async def inline_manus():
    keyboard = InlineKeyboardBuilder()
    for man in manus:
        keyboard.add(InlineKeyboardButton(text=man, url='https://github.com/Platonn3'))
    return keyboard.adjust(1).as_markup()

