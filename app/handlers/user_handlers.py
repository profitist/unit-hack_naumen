from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.validators as val
import database.requests.requests as rq
import app.keyboards as kb
import utils.text_utils as tu
from source.user import UserClass

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


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    is_admin = await rq.is_admin(message.from_user.id)
    if is_admin:
        await message.answer(tu.send_start_admin_user_message(message),
                             reply_markup=kb.admin_menu)
    else:
        await message.answer(tu.send_start_common_user_message(message),
                             reply_markup=kb.main_reply)


@user_router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("help")


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


@user_router.message(F.text == "⬅️ Назад")
async def go_back(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == Reg.second_name:
        await state.set_state(Reg.first_name)
        await message.answer("Введите имя (только буквы, от 2 до 30 символов):", reply_markup=kb.back_reply)

    elif current_state == Reg.number:
        await state.set_state(Reg.second_name)
        await message.answer("Введите фамилию (только буквы, от 2 до 30 символов):", reply_markup=kb.back_reply)

    else:
        await message.answer("Вы вышли из регистрации", reply_markup=kb.main_reply)
        await state.clear()


@user_router.message(F.text == "Зарегистрироваться ✔")
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(Reg.first_name)
    await message.answer("Введите имя (только буквы, от 2 до 30 символов)",
                         reply_markup=kb.back_reply)


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
                         reply_markup=kb.back_reply)


@user_router.message(Reg.first_name)
async def reg_two(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        return await go_back(message, state)
    if not val.is_valid_first_name(message.text):
        await message.answer("❌ Некорректное имя! Используйте только буквы (2-30 символов). Попробуйте еще раз:"
                             ,reply_markup=kb.back_reply)
        return

    await state.update_data(first_name=message.text)
    await state.set_state(Reg.second_name)
    await message.answer('✅ Принято! Теперь введите фамилию (только буквы, от 2 до 30 символов)'
                         ,reply_markup=kb.back_reply)


@user_router.message(Reg.second_name)
async def reg_three(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        return await go_back(message, state)

    if not val.is_valid_second_name(message.text):
        await message.answer("❌ Некорректная фамилия! Используйте только буквы (2-30 символов). Попробуйте еще раз:"
                             ,reply_markup=kb.back_reply)
        return

    await state.update_data(second_name=message.text)
    await state.set_state(Reg.number)
    await message.answer('✅ Принято! Теперь введите номер телефона в формате +79991234567 или 89991234567'
                         ,reply_markup=kb.back_reply)


@user_router.message(Reg.number)
async def reg_four(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        return await go_back(message, state)

    if not val.is_valid_phone_number(message.text):
        await message.answer(
            "❌ Некорректный номер! Введите в формате +79991234567 или 89991234567. Попробуйте еще раз:"
         ,reply_markup=kb.back_reply)
        return

    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(
        f'✅ Регистрация завершена!\n'
        f'Имя: {data["first_name"]}\n'
        f'Фамилия: {data["second_name"]}\n'
        f'Номер: {data["number"]}',
        reply_markup=kb.reply_test
    )
    await state.clear()

