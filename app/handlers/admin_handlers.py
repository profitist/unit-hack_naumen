from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.validators as val
import database.requests.requests as rq
import app.keyboards as kb
import utils.text_utils as tu
from utils.admin_utils import admin_required
from source.working_classes import Event

admin_router = Router()


class AddEvent(StatesGroup):
    title = State()
    description = State()
    date = State()
    vacant_places = State()
    address = State()


@admin_router.message(F.text == 'Добавить новое событие')
@admin_required
async def add_event_1(message: Message, state: FSMContext):
    await state.set_state(AddEvent.title)
    await message.answer(text='Пора добавить новое событие!'
                              ' Введите имя события:')


@admin_router.message(AddEvent.title)
@admin_required
async def add_event_2(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(title=answer)
    await state.set_state(AddEvent.description)
    await message.answer(text='Введите описание события!')


@admin_router.message(AddEvent.description)
@admin_required
async def add_event_3(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(description=answer)
    await state.set_state(AddEvent.date)
    await message.answer(text='Отлично, описание добавлено\n!'
                              'Давайте назначим дату: Введите ее в формате '
                              '{дд.мм.гггг}')


@admin_router.message(AddEvent.date)
@admin_required
async def add_event_4(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(date=answer)
    await state.set_state(AddEvent.vacant_places)
    await message.answer(text=f'Ура! {state.get_value("title")} '
                              f'будет проведен {state.get_value("date")}\n\n'
                              f'Давай укажем максимальное число участников')


@admin_router.message(AddEvent.vacant_places)
@admin_required
async def add_event_5(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(vacant_places=answer)
    await state.set_state(AddEvent.address)
    await message.answer(text='Давай укажем адреc, '
                              'по которому будет проводиться Ивент')


@admin_router.message(AddEvent.address)
@admin_required
async def add_event_end(message: Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    data = state.get_data()
    event = Event(_title=data['title'], _description=data['description'],
                  _start_time=data['date'], _vacant_places=data['vacant_places'],
                  _location=data['address'])

    await state.clear()











