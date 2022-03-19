from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from loguru import logger
from app.services.users import User


# TODO: добавить валидацию в форму
class SendVideo(StatesGroup):
    """Форма для сохранения состояния данных"""

    first_name = State()
    last_name = State()
    email = State()
    phone = State()
    title = State()
    description = State()
    video_url = State()


async def start_send_video(message: types.Message):
    """Срабатывает при нажатии на кнопку 'Отправить видео'"""

    await SendVideo.first_name.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*['Отменить'])
    await message.answer('Имя:', reply_markup=keyboard)


async def waiting_first_name(message: types.Message, state: FSMContext):
    """Срабатывает при вводе first_name"""

    await state.update_data(first_name=message.text)
    await SendVideo.next()
    await message.answer('Фамилия:')


async def waiting_last_name(message: types.Message, state: FSMContext):
    """Срабатывает при вводе last_name"""

    await state.update_data(last_name=message.text)
    await SendVideo.next()
    await message.answer('Email:')


async def waiting_email(message: types.Message, state: FSMContext):
    """Срабатывает при вводе email"""

    await state.update_data(email=message.text)
    await SendVideo.next()
    await message.answer('Номер телефона:')


async def waiting_phone(message: types.Message, state: FSMContext):
    """Срабатывает при вводе phone"""

    await state.update_data(phone=message.text)
    await SendVideo.next()
    await message.answer('Заголовок:')


async def waiting_title(message: types.Message, state: FSMContext):
    """Срабатывает при вводе title"""

    await state.update_data(title=message.text)
    await SendVideo.next()
    await message.answer('Описание:')


async def waiting_description(message: types.Message, state: FSMContext):
    """Срабатывает при вводе description"""

    await state.update_data(description=message.text)
    await SendVideo.next()
    await message.answer('Отправить видео:')


async def waiting_video(message: types.Message, state: FSMContext):
    """Срабатывает при отправке video"""

    user = User(message.from_user.id)
    video_url = await message.video.get_url()
    await state.update_data(video_url=video_url)
    data = await state.get_data()
    is_save_video = user.save_video(data)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*(['Отправить видео']))
    if is_save_video:
        text = 'Ваше видео принято'
    else:
        text = 'Ошибка попробуйте позже'
    await message.answer(text, reply_markup=keyboard)
    await state.finish()


def register_send_video_handlers(dp: Dispatcher):
    """Регистрация команд"""

    dp.register_message_handler(start_send_video, commands='video', state='*')
    dp.register_message_handler(start_send_video, Text(equals="отправить видео", ignore_case=True), state='*')
    dp.register_message_handler(waiting_first_name, state=SendVideo.first_name)
    dp.register_message_handler(waiting_last_name, state=SendVideo.last_name)
    dp.register_message_handler(waiting_email, state=SendVideo.email)
    dp.register_message_handler(waiting_phone, state=SendVideo.phone)
    dp.register_message_handler(waiting_title, state=SendVideo.title)
    dp.register_message_handler(waiting_description, state=SendVideo.description)
    dp.register_message_handler(waiting_video, content_types=['video'], state=SendVideo.video_url)
