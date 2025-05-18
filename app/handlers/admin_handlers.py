from datetime import datetime, timedelta

from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from aiogram import Bot, F, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from io import BytesIO
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import app.validators as val
from database.models.models import MasterClass
from database.session import AsyncSessionLocal
from utils.admin_utils import admin_required
from source.working_classes import Event, Activity
import asyncio
from database.requests.requests import add_event_if_not_exists
import app.keyboards.admin_keyboards as ak
import database.requests.requests as rq
import utils.text_utils as tu
import aiofiles
import uuid
import os

admin_router = Router()
scheduler = AsyncIOScheduler()


class AddEvent(StatesGroup):
    title = State()
    description = State()
    date = State()
    vacant_places = State()
    address = State()
    photo = State()
    send = State()

class AddMasterClass(StatesGroup):
    event_id = State()
    title = State()
    description = State()
    date = State()
    vacant_places = State()
    photo = State()


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
        if counter <= 0:
            raise ValueError
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
        await message.answer("Событие добавлено. Всех зарегистрировавшихся уведомят за час!",
                             reply_markup=ak.send_everyone_event_creation)
        broadcast_time = event._start_time - timedelta(hours=1)
        scheduler.add_job(
            send_event_broadcast,
            'date',
            run_date=broadcast_time,
            args=[event, message.bot]
        )
        await state.set_state(AddEvent.send)
    else:
        await message.answer(text='Некорректный адрес, попробуй ввести еще раз')

async def send_event_broadcast(event: Event, bot: Bot):
    message_text = (
        f"Уже через час!  *{event._title}*!\n"
        f"📍 Где: {event._location}\n"
        f"ℹ {event._description}\n"
        "Не пропустите!"
    )
    users = await rq.get_registered_users_for_event()
    for user_id in users:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=message_text,
                parse_mode="Markdown"
            )
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"{e} for user {user_id}")


@admin_router.message(
    F.text == 'Уведомить всех о новом событии',
    AddEvent.send  # Проверяем состояние
)
@admin_required
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
        await send_message_to_everybody(message, message.bot, broadcast_message)
        await state.clear()
    else:
        await message.answer(text='Сообщение не может быть пустым. Попробуйте еще раз.')


async def send_message_to_everybody(
        message: Message, bot: Bot, broadcast_message: str):
    users = await rq.get_all_tg_ids()
    success_count = 0
    fail_count = 0
    await message.answer(text='Рассылка о событии началась...',
                         reply_markup=ReplyKeyboardRemove())
    for user_id in users:
        try:
            print(user_id)
            await bot.send_message(chat_id=user_id, text=broadcast_message)
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            fail_count += 1

    await message.answer(text='Рассылка завершена!', reply_markup=ak.admin_menu)


@admin_router.message(F.text == 'Добавить новый мастер класс')
@admin_required
async def start_add_master_class(message: Message, state: FSMContext):
    events = await rq.show_all_events()
    if not events:
        await message.answer("Нет доступных мероприятий для привязки мастер-класса",
                             reply_markup=ak.admin_menu)
        return

    await state.set_state(AddMasterClass.event_id)
    await message.answer("Выберите мероприятие:",
                         reply_markup=await ak.inline_events_names(events))


@admin_router.callback_query(F.data.startswith('chose_event_'), AddMasterClass.event_id)
@admin_required
async def select_event_for_master_class(callback: CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split('_')[-1])
    await state.update_data(event_id=event_id)
    await state.set_state(AddMasterClass.title)
    await callback.message.answer("Введите название мастер-класса:")
    await callback.answer()


@admin_router.message(AddMasterClass.title)
@admin_required
async def add_master_class_title(message: Message, state: FSMContext):
    if val.is_valid_event_name(message.text):
        await state.update_data(title=message.text)
        await state.set_state(AddMasterClass.description)
        await message.answer("Введите описание мастер-класса:")
    else:
        await message.answer("Некорректное название. Попробуйте еще раз.")


@admin_router.message(AddMasterClass.description)
@admin_required
async def add_master_class_description(message: Message, state: FSMContext):
    if len(message.text) >= 10:
        await state.update_data(description=message.text)
        await state.set_state(AddMasterClass.date)
        await message.answer("Введите дату и время мастер-класса (формат: дд.мм.гггг чч:мм):")
    else:
        await message.answer("Описание слишком короткое. Минимум 10 символов.")


@admin_router.message(AddMasterClass.date)
@admin_required
async def add_master_class_date(message: Message, state: FSMContext):
    if val.is_valid_event_date(message.text):
        try:
            date = datetime.strptime(message.text, '%d.%m.%Y %H:%M:%S')
            await state.update_data(date=date)
            await state.set_state(AddMasterClass.vacant_places)
            await message.answer("Введите количество доступных мест:")
        except ValueError:
            await message.answer("Некорректный формат времени. Используйте дд.мм.гггг чч:мм")
    else:
        await message.answer("Некорректный формат даты. Используйте дд.мм.гггг чч:мм")


@admin_router.message(AddMasterClass.vacant_places)
@admin_required
async def add_master_class_places(message: Message, state: FSMContext):
    try:
        places = int(message.text)
        if places <= 0:
            raise ValueError
        await state.update_data(vacant_places=places)

        # Получаем все данные
        data = await state.get_data()

        # Создаем и сохраняем мастер-класс
        master_class = MasterClass(
            event_id=data['event_id'],
            title=data['title'],
            description=data['description'],
            datetime=data['date'],
            vacant_places=data['vacant_places'],
        )

        async with AsyncSessionLocal() as session:
            session.add(master_class)
            await session.commit()

        await message.answer("Мастер-класс успешно добавлен!",
                             reply_markup=ak.admin_menu)
        await state.clear()

    except ValueError:
        await message.answer("Введите корректное число мест (больше 0)")

class FaqAdd(StatesGroup):
    message = State()
    apply = State()


@admin_router.message(F.text == 'Создать FAQ')
@admin_required
async def add_faq_question(message: Message, state: FSMContext):
    await message.answer('Введите текст вопроса 😊')
    await state.set_state(FaqAdd.message)


@admin_router.message(FaqAdd.message)
@admin_required
async def add_faq_answer(message: Message, state: FSMContext):
    await state.update_data(faq_question=message.text)
    await state.set_state(FaqAdd.apply)
    await message.answer(text='Введите ответ на вопрос: 😊')


@admin_router.message(FaqAdd.apply)
@admin_required
async def add_faq_answer(message: Message, state: FSMContext):
    await state.update_data(faq_answer=message.text)
    data = await state.get_data()
    await state.set_state(FaqAdd.message)
    await message.answer(text=f'FAQ добавлен, проверьте содержимое:\n'
                              f'Вопрос: {data["faq_question"]}\n\n'
                              f'Ответ: {data["faq_answer"]}\n\n'
                              f'Добавить вопрос?',
                         reply_markup=ak.accept_add_faq)


@admin_router.callback_query(F.data == 'accept_add_faq')
@admin_required
async def accept_add_faq_callback_query(
        callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await rq.add_faq(data['faq_question'], data['faq_answer'])
    await callback.message.answer('Вопрос добавлен ✅',
                                  reply_markup=ak.admin_menu)
    await state.clear()


@admin_router.callback_query(F.data == 'deny_add_faq')
@admin_required
async def deny_add_faq_callback_query(
        callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Создание вопроса отменено ❌',
                                  reply_markup=ak.admin_menu)
    await state.clear()
