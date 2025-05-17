from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.validators as val
import database.requests.requests as rq
import app.keyboards as kb
import utils.text_utils as tu
from handlers import router


@router.message(Command('add_event'))
async def add_event(message: Message):
    await message.answer(text='Пора добавить новое событие!')