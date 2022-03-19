from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from app.services.users import User


async def cmd_start_stop(message: types.Message, state: FSMContext):
    """Выводит следующие кнопки после команд /start /stop"""

    await state.finish()
    user = User(message.from_user['id'])
    if user.is_register():
        answer, buttons = f'Привет, {user.get_name()} отправьте видео', ['Отправить видео']
    else:
        answer, buttons = 'Привет, пройдите регистрацию', ['Регистрация']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer(answer, reply_markup=keyboard)


def register_base_handlers(dp: Dispatcher):
    """Регистрация команд"""

    dp.register_message_handler(cmd_start_stop, commands="start", state="*")
    dp.register_message_handler(cmd_start_stop, commands="cancel", state="*")
    dp.register_message_handler(cmd_start_stop, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_start_stop, Text(equals="Отменить", ignore_case=True), state="*")
