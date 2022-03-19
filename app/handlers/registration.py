import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.services.users import User


class RegisterForm(StatesGroup):
    """Форма регистрации"""

    name = State()
    phone = State()


async def register_start(message: types.Message):
    """ Срабатывает при регистрации '/register'"""

    user = User(message.from_user.id)
    if user.is_register():
        text, buttons = 'Вы уже зарегистрированы', ['Отправить видео']
    else:
        text, buttons = 'Ваше имя:', ['Отменить']
        await RegisterForm.name.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer(text, reply_markup=keyboard)


# TODO: добавить валидацию
async def user_name(message: types.Message, state: FSMContext):
    """Срабатывает после ввода имени"""

    await state.update_data(name=message.text)
    await RegisterForm.next()
    await message.answer('Номер телефона:')


# TODO: добавить валидацию
async def user_phone(message: types.Message, state: FSMContext):
    """ Срабатывает после ввода телефона"""

    await state.update_data(phone=message.text)
    user = User(message.from_user.id)
    data = await state.get_data()
    is_register = user.register_user(name=data['name'], phone=data['phone'])
    if is_register:
        answer, buttons = 'Мы можете отправить видео', ['Отправить видео']
    else:
        answer, buttons = 'Ошибка при регистрации попробуйте чуть позже', ['Регистрация']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer(answer, reply_markup=keyboard)
    await state.finish()


def register_user_registration_handlers(dp: Dispatcher):
    """Регистрация команд"""

    dp.register_message_handler(register_start, Text(equals='регистрация', ignore_case=True), state='*')
    dp.register_message_handler(register_start, commands='register', state='*')
    dp.register_message_handler(user_name, state=RegisterForm.name)
    dp.register_message_handler(user_phone, state=RegisterForm.phone)
