from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить новое событие")],
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
