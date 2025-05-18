from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
        ReplyKeyboardMarkup, KeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить новое событие")],
        [KeyboardButton(text="Добавить новый мастер класс")],
        [KeyboardButton(text="Проверить QR-код")],
        [KeyboardButton(text="Актуальные события 🗓")],
        [KeyboardButton(text="Сделать рассылку"),
         KeyboardButton(text='Создать FAQ')]
    ],
    resize_keyboard=True
)


send_everyone_event_creation = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Уведомить всех о новом событии')]
    ]
)

accept_add_faq = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅', callback_data='accept_add_faq'),
         InlineKeyboardButton(text='❌', callback_data='deny_add_faq')]
    ]
)


async def inline_events_names(events):
    keyboard = InlineKeyboardBuilder()
    for event in events:
        keyboard.add(InlineKeyboardButton(text=f'{event.title}', callback_data=f'chose_event_{event.id}'))
    return keyboard.adjust(1).as_markup()
