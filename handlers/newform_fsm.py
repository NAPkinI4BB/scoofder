from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

from database.connectDB_class import ConnectDB
from lexicon.lexicon import LEXICON
import os

storage = MemoryStorage()

router: Router = Router()

CALLBACK_DICT = {
    'sex': ['male', 'female'],
    'course': ['first', 'second', 'third', 'fourth', 'other', 'notFGIG']
}


class NewformFSM(StatesGroup):
    enter_name = State()
    enter_sex = State()
    enter_course = State()
    awaiting_photo = State()


@router.message(Command(commands=['newform']), StateFilter(default_state))
async def process_command_newform(message: Message, state: FSMContext):
    await message.answer(LEXICON.get('/newform'))
    await message.answer(text='Введите имя')
    await state.set_state(NewformFSM.enter_name)


@router.message(Command(commands=['newform']))
async def process_command_newform_in_state(message: Message):
    await message.answer(text='Вы сейчас в процессе создания анкеты. Выйти из него можно командой /cancel')


@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_command_cancel_in_state(message: Message, state: FSMContext):
    await message.answer(LEXICON.get('/cancel'))
    await state.clear()


@router.message(Command(commands=['cancel']))
async def process_command_cancel(message: Message):
    await message.answer(text='Ты посев. Отменять нечего')


@router.message(F.text, StateFilter(NewformFSM.enter_name))
async def enter_name_process(message: Message, state: FSMContext):
    await message.answer(f'{message.text}, приятно познакомиться)))')
    await state.update_data(name=message.text)
    male_btn = InlineKeyboardButton(text='Мужской', callback_data='male')
    female_btn = InlineKeyboardButton(text='Женский', callback_data='female')
    keyboard: list[list[InlineKeyboardButton]] = [
        [male_btn, female_btn]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(text='Теперь введи свой пол, основываясь на том, что имеешь между ног',
                         reply_markup=markup)
    await state.set_state(NewformFSM.enter_sex)


@router.callback_query(StateFilter(NewformFSM.enter_sex), F.data.in_(CALLBACK_DICT.get('sex')))
async def enter_sex_process(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    await state.update_data(sex=callback.data)

    fst_button = InlineKeyboardButton(text='1', callback_data='first')
    sec_button = InlineKeyboardButton(text='2', callback_data='second')
    thrd_button = InlineKeyboardButton(text='3', callback_data='third')
    fth_button = InlineKeyboardButton(text='4', callback_data='fourth')
    other_button = InlineKeyboardButton(text='Другое', callback_data='other')
    not_fgig_button = InlineKeyboardButton(text='Не ФГиГ (хочу девочку с ФГиГа)', callback_data='notFGIG')
    keyboard: list[list[InlineKeyboardButton]] = [
        [fst_button, sec_button, thrd_button, fth_button],
        [other_button],
        [not_fgig_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await callback.message.answer(text='На каком курсе учишься?))', reply_markup=markup)
    await callback.answer()
    await state.set_state(NewformFSM.enter_course)


@router.callback_query(StateFilter(NewformFSM.enter_course), F.data.in_(CALLBACK_DICT.get('course')))
async def enter_course_process(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    await state.update_data(course=callback.data)
    await callback.message.answer(text='пришли свое фото. (я если что привыкла с точками писать, это круто)')
    await callback.answer()
    await state.set_state(NewformFSM.awaiting_photo)


@router.message(StateFilter(NewformFSM.awaiting_photo), F.photo)
async def send_photo_process(message: Message, state: FSMContext):
    photo: PhotoSize = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = f'photos/{message.from_user.id}.jpg'
    print(message.from_user.id)
    await state.update_data(photo_path=message.from_user.id)
    os.makedirs('photos', exist_ok=True)
    await message.bot.download_file(file.file_path, file_path)
    user_data = await state.get_data()
    message.db.write_user_data(user_data=user_data)
    await message.answer(text=f'{user_data}')
    await state.clear()

    db: ConnectDB = message.bot['db']
    await db.write_user_data(user_data)


