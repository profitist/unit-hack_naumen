from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import database.requests.requests as rq
import app.keyboards as kb
import utils.text_utils as tu

router = Router()


class Reg(StatesGroup):
    name = State()
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
    is_admin = rq.is_admin(message.from_user.id)
    if is_admin:
        await message.answer(tu.send_start_admin_user_message(message),
                             reply_markup=kb.main_reply)
    else:
        await message.answer(tu.send_start_common_user_message(message),
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
    await state.set_state(Reg.name)
    await message.answer("Введите имя", reply_markup=ReplyKeyboardRemove())


@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите имя', reply_markup=ReplyKeyboardRemove())


@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона в формате +71234567890')


@router.message(Reg.number)
async def two_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Спасибо, родной.\nИмя: {data["name"]}\nНомер: {data["number"]}', reply_markup=kb.reply_test)
    await state.clear()