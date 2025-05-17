from datetime import datetime

from aiogram.types import Message, InlineKeyboardMarkup
from aiogram import Bot
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.validators as val
from utils.admin_utils import admin_required
from source.working_classes import Event
import asyncio
from database.requests.requests import add_event_if_not_exists
import app.keyboards.admin_keyboards as ak
import database.requests.requests as rq
import utils.text_utils as tu

admin_router = Router()


class AddEvent(StatesGroup):
    title = State()
    description = State()
    date = State()
    vacant_places = State()
    address = State()
    send = State()


class Broadcast(StatesGroup):
    message = State()


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
    if val.is_valid_event_name(answer):
        await state.update_data(title=answer)
        await state.set_state(AddEvent.description)
        await message.answer(text='Введите описание события!')
    else:
        await message.answer(text='Введенный заголовок не валиден')


@admin_router.message(AddEvent.description)
@admin_required
async def add_event_3(message: Message, state: FSMContext):
    answer = message.text
    if len(answer) >= 10:
        await state.update_data(description=answer)
        await state.set_state(AddEvent.date)
        await message.answer(text='Отлично, описание добавлено!\n'
                                  'Давайте назначим дату: Введите ее в формате '
                                  '{дд.мм.гггг}')
    else:
        await message.answer(text='Описание слишком короткое, '
                                  'давай дадим больше информации')


@admin_router.message(AddEvent.date)
@admin_required
async def add_event_4(message: Message, state: FSMContext):
    answer = message.text
    if val.is_valid_event_date(answer):
        date = datetime.strptime(answer, '%d.%m.%Y %H:%M:%S')
        await state.update_data(date=date)
        await state.set_state(AddEvent.vacant_places)
        await message.answer(text=f'Ура! {await state.get_value("title")} '
                                  f'будет проведен {await state.get_value("date")}\n\n'
                                  f'Давай укажем максимальное число участников')
    else:
        await message.answer('Введенная дата не корректна!\n'
                             'Попробуй ввести еще раз\n\n'
                             'Вот формат: {дд.мм.гг чч:мин}')


@admin_router.message(AddEvent.vacant_places)
@admin_required
async def add_event_5(message: Message, state: FSMContext):
    answer = message.text
    try:
        counter = int(answer)
        await state.update_data(vacant_places=counter)
        await state.set_state(AddEvent.address)
        await message.answer(text='Давай укажем адреc, '
                                  'по которому будет проводиться Ивент')
    except ValueError:
        await message.answer(text='Некорректный ввод!\n '
                                  'Проверь, что вводишь число!')


@admin_router.message(AddEvent.address)
@admin_required
async def add_event_end(message: Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    data = await state.get_data()
    if val.is_valid_location(address):
        event = Event(_title=data['title'], _description=data['description'],
                      _start_time=data['date'],
                      _vacant_places=data['vacant_places'],
                      _location=data['address'])
        await add_event_if_not_exists(event)
        await message.answer("Событие добавлено",
                             reply_markup=ak.send_everyone_event_creation)
        await state.set_state(AddEvent.send)
    else:
        await message.answer(text='Некорректный адрес, попробуй ввести еще раз')


@admin_router.message(
    F.text == 'Уведомить всех о новом событии',
    AddEvent.send  # Проверяем состояние
)
@admin_router.message(AddEvent.send)
async def send_everybody_event_info(message: Message, state: FSMContext):
    data = await state.get_data()
    text = tu.send_notification_of_creating_event(data)
    await send_message_to_everybody(message.bot, text)
    await state.clear()


@admin_router.message(F.text == "Сделать рассылку")
@admin_required
async def start_broadcast(message: Message, state: FSMContext):
    await state.set_state(Broadcast.message)
    await message.answer(text='Введите текст сообщения для рассылки:')


@admin_router.message(Broadcast.message)
@admin_required
async def send_broadcast(message: Message, state: FSMContext):
    broadcast_message = message.text
    if len(broadcast_message) > 0:
        await send_message_to_everybody(message.bot, broadcast_message)
        await state.clear()
    else:
        await message.answer(text='Сообщение не может быть пустым. Попробуйте еще раз.')


async def send_message_to_everybody(bot: Bot, broadcast_message: str):
    users = await rq.get_all_tg_ids()
    success_count = 0
    fail_count = 0

    for user_id in users:
        try:
            print(user_id)
            await bot.send_message(chat_id=user_id, text=broadcast_message)
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            fail_count += 1

