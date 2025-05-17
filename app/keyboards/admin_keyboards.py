from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton

send_everyone_event_creation = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Уведомить всех о новом событии')]
    ]
)
