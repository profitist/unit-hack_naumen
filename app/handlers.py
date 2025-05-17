from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.validators as val

import app.keyboards as kb

router = Router()


class Reg(StatesGroup):
    first_name = State()
    second_name = State()
    number = State()

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