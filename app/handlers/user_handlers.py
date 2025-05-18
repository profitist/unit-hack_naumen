from aiogram.dispatcher import router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import (Message,
                           CallbackQuery,
                           BotCommand,
                           ReplyKeyboardRemove)
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.validators as val
import database.requests.requests as rq
import app.keyboards.keyboards as kb
import app.keyboards.admin_keyboards as ak
import utils.text_utils as tu
from source.user import UserClass
from database.requests.requests import add_user_if_not_exists

ADMIN_CHAT_ID = -1002649837821
# ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
# ADMIN_CHAT_ID = dotenv_values('env').get('ADMIN_CHAT_ID')


user_router = Router()


class Reg(StatesGroup):
    first_name = State()
    second_name = State()
    number = State()


class Ask(StatesGroup):
    waiting_for_question = State()


async def set_commands(bot):
    commands = [
        BotCommand(command="/start_chat", description="Начало работы"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/reg", description="Регистрация"),
    ]
    await bot.set_my_commands(commands)



@user_router.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject):
    if command.args is None:
        is_admin = await rq.is_admin(message.from_user.id)
        if is_admin:
            await message.answer(tu.send_start_admin_user_message(message),
                                 reply_markup=kb.admin)
        else:
            await message.answer(tu.send_start_common_user_message(message),
                                 reply_markup=kb.main_reply)
    if command.args == 'test':
        await message.answer("Вот тебе помощь!")


@user_router.message(Command("start_chat"))
async def get_start(message: Message):
    is_admin = await rq.is_admin(message.from_user.id)
    if is_admin:
        await message.answer(tu.send_start_admin_user_message(message),
                             reply_markup=ak.admin_menu)
    else:
        await message.answer(tu.send_start_common_user_message(message),
                             reply_markup=kb.main_reply)


@user_router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("help")

@user_router.message(F.text == "О нас ℹ️")
async def get_info(message: Message):
    await message.answer(
        'Я Бот - организатор мероприятий компании Naumen 😊\n\n'
        'Помогу тебе узнать всю информацию о предстоящих мероприятиях'
        'нашей компании, а также при желании зарегистрироваться на них.'
    )


# Запрос вопроса
@user_router.message(F.text == "Задать вопрос")
async def ask_question(message: Message, state: FSMContext):
    await state.set_state(Ask.waiting_for_question)
    await message.answer("Напишите свой вопрос:", reply_markup=ReplyKeyboardRemove())


# Получение и пересылка вопроса админу
@user_router.message(Ask.waiting_for_question)
async def got_question(message: Message, state: FSMContext, bot):
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"
    text = message.text

    # Отправим сообщение админу с user_id
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Вопрос от @{username} (ID: {user_id}):\n{text}"
    )

    await message.answer("Ваш вопрос отправлен. Мы скоро ответим!", reply_markup=kb.main_reply)
    await state.clear()


@user_router.message(F.chat.id == ADMIN_CHAT_ID)
async def reply_to_user(message: Message, bot):
    if message.reply_to_message:
        # Ищем user_id в оригинальном сообщении
        lines = message.reply_to_message.text.splitlines()
        for line in lines:
            if "ID:" in line:
                try:
                    user_id = int(line.split("ID:")[1].strip().replace(")", "").replace(":", ""))
                    await bot.send_message(chat_id=user_id, text=f"Ответ от администратора:\n{message.text}")
                    await message.answer("✅ Ответ отправлен пользователю.")
                except Exception as e:
                    await message.answer(f"❌ Ошибка отправки: {e}")
                break
        else:
            await message.answer("❌ Не найден ID пользователя в сообщении.")
    else:
        await message.answer("ℹ️ Ответ должен быть *на сообщение с вопросом*.", parse_mode="Markdown")



# @router.callback_query(F.data == 'registration')
# async def registration(callback:CallbackQuery):
#     # TO DO
#     # тут взаимодейтвие с бд для регистрации
#     await callback.answer('')
#     await callback.message.edit_text('Ты зареган!иди гулйя га меро', reply_markup=await kb.inline_manus())


@user_router.callback_query(F.data == "back_in_reg")
async def go_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == Reg.second_name:
        await state.set_state(Reg.first_name)
        await callback.answer('')
        await callback.message.answer("Введите имя (только буквы, от 2 до 30 символов):", reply_markup=kb.reg_back_inline)

    elif current_state == Reg.number:
        await state.set_state(Reg.second_name)
        await callback.answer('')
        await callback.message.answer("Введите фамилию (только буквы, от 2 до 30 символов):", reply_markup=kb.reg_back_inline)

    else:
        await callback.answer('')
        await callback.message.answer("Вы вышли из регистрации", reply_markup=kb.main_reply)
        await state.clear()


@user_router.message(F.text == "Зарегистрироваться ✔")
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(Reg.first_name)
    await message.answer("Введите имя (только буквы, от 2 до 30 символов)",
                         reply_markup=kb.reg_back_inline)


@user_router.message(F.text == "Мой профиль")
async def start_registration(message: Message):
    await message.answer("Это твой профиль."
                         "\nТут ты можешь узнать, на какие мероприятия ты записался, какой ты в очереди, получить QR-код на мероприятие"
                         "\nТак же ты можешь проверить и исправить свои данные,",
                         reply_markup=kb.profile_reply)
    # TO DO
    # Список активностей в которых зареган
    # Список очередей в которых находится
    # Данные


@user_router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.first_name)
    await message.answer('Введите имя (только буквы, от 2 до 30 символов)',
                         reply_markup=kb.reg_back_inline)


@user_router.message(Reg.first_name)
async def reg_two(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        return await go_back(message, state)
    if not val.is_valid_first_name(message.text):
        await message.answer("❌ Некорректное имя! Используйте только буквы (2-30 символов). Попробуйте еще раз:"
                             , reply_markup=kb.reg_back_inline)
        return

    await state.update_data(first_name=message.text)
    await state.set_state(Reg.second_name)
    await message.answer('✅ Принято! Теперь введите фамилию (только буквы, от 2 до 30 символов)'
                         , reply_markup=kb.reg_back_inline)


@user_router.message(Reg.second_name)
async def reg_three(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        return await go_back(message, state)

    if not val.is_valid_second_name(message.text):
        await message.answer("❌ Некорректная фамилия! Используйте только буквы (2-30 символов). Попробуйте еще раз:"
                             , reply_markup=kb.reg_back_inline)
        return

    await state.update_data(second_name=message.text)
    await state.set_state(Reg.number)
    await message.answer('✅ Принято! Теперь введите номер телефона в формате +79991234567 или 89991234567'
                         , reply_markup=kb.reg_back_inline)


@user_router.message(Reg.number)
async def reg_four(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        return await go_back(message, state)

    if not val.is_valid_phone_number(message.text):
        await message.answer(
            "❌ Некорректный номер! Введите в формате +79991234567 или 89991234567. Попробуйте еще раз:"
         ,reply_markup=kb.reg_back_inline)
        return

    await state.update_data(number=message.text)
    data = await state.get_data()
    user = UserClass(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=data["first_name"],
        last_name=data["second_name"],
        phone=data["number"],
        is_admin=False
    )
    await add_user_if_not_exists(user)

    await message.answer(
        f'✅ Регистрация завершена!\n'
        f'Имя: {data["first_name"]}\n'
        f'Фамилия: {data["second_name"]}\n'
        f'Номер: {data["number"]}',
        reply_markup=kb.reply_test
    )
    await state.clear()


@user_router.message(F.text == "Актуальные события 🗓")
async def get_all_events(message: Message):
    events = await rq.show_all_events()
    for event in events:
        await message.answer(
            f'{event.description}\n'
            f'{event.datetime}'
            " <a href='https://t.me/naume_pivo_n_bot?start=test'>Подробнее</a>",
            parse_mode="HTML"
        )


@user_router.message(F.text.startswith('FAQ'))
async def faq(message: Message):
    faqs = await rq.get_faq()
    if not faqs:
        await message.answer('Мы никомы не нужны',
                             reply_markup=kb.main_reply)
        return
    text_message = ''
    print(faqs[0].question)
    print(faqs[1].question)
    for faq in faqs:
        text_message += faq.question + '\n\n'
        text_message += faq.answer
    await message.answer(text_message, reply_markup=kb.main_reply)
