import os

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.validators as val

import app.keyboards as kb

ADMIN_CHAT_ID = -1002649837821
# ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
# ADMIN_CHAT_ID = dotenv_values('env').get('ADMIN_CHAT_ID')


router = Router()


class Reg(StatesGroup):
    first_name = State()
    second_name = State()
    number = State()

class Ask(StatesGroup):
    waiting_for_question = State()

async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Начало работы"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/reg", description="Регистрация"),
    ]
    await bot.set_my_commands(commands)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}",
                         reply_markup=kb.main_reply)

@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("help")


# Запрос вопроса
@router.message(F.text == "Задать вопрос")
async def ask_question(message: Message, state: FSMContext):
    await state.set_state(Ask.waiting_for_question)
    await message.answer("Напишите свой вопрос:", reply_markup=ReplyKeyboardRemove())


# Получение и пересылка вопроса админу
@router.message(Ask.waiting_for_question)
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


@router.message(F.chat.id == ADMIN_CHAT_ID)
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


@router.message(F.text == "Зарегистрироваться")
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(Reg.first_name)
    await message.answer("Введите имя (только буквы, от 2 до 30 символов)",
                         reply_markup=ReplyKeyboardRemove())


@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.first_name)
    await message.answer('Введите имя (только буквы, от 2 до 30 символов)',
                         reply_markup=ReplyKeyboardRemove())


@router.message(Reg.first_name)
async def reg_two(message: Message, state: FSMContext):
    if not val.is_valid_first_name(message.text):
        await message.answer("❌ Некорректное имя! Используйте только буквы (2-30 символов). Попробуйте еще раз:")
        return

    await state.update_data(first_name=message.text)
    await state.set_state(Reg.second_name)
    await message.answer('✅ Принято! Теперь введите фамилию (только буквы, от 2 до 30 символов)')


@router.message(Reg.second_name)
async def reg_three(message: Message, state: FSMContext):
    if not val.is_valid_second_name(message.text):
        await message.answer("❌ Некорректная фамилия! Используйте только буквы (2-30 символов). Попробуйте еще раз:")
        return

    await state.update_data(second_name=message.text)
    await state.set_state(Reg.number)
    await message.answer('✅ Принято! Теперь введите номер телефона в формате +79991234567 или 89991234567')


@router.message(Reg.number)
async def reg_four(message: Message, state: FSMContext):
    if not val.is_valid_phone_number(message.text):
        await message.answer(
            "❌ Некорректный номер! Введите в формате +79991234567 или 89991234567. Попробуйте еще раз:")
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