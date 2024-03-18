from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import ReplyKeyboardRemove
from filters.type_of_chat import ChatTypeFilter
from keyboards.for_navigate import keyboard
from aiogram.utils.formatting import as_marked_section, Bold, TextLink
private_router = Router()
private_router.message.filter(ChatTypeFilter(['private']))


@private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('this answer for start command', reply_markup=keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Choose your command'
    ))


@private_router.message(or_f(Command('options'), F.text.lower() == 'options'))
async def options_cmd(message: types.Message):
    await message.answer('options list', reply_markup=ReplyKeyboardRemove())


@private_router.message(Command('about'))
async def options_cmd(message: types.Message):
    await message.answer('info about <b><u>bot</u></b>')


@private_router.message(or_f(Command('links'), F.text.lower() == 'links'))
async def options_cmd(message: types.Message):
    text = as_marked_section(
        Bold('Active links'),
        TextLink('study bot', url='https://t.me/GoITeens_Study_bot'),
        TextLink('tech google meet', url='https://meet.google.com/mvq-sahu-szm'),
        marker='🎗'
    )
    await message.answer(text.as_html())


@private_router.message((F.text.lower() == 'розклад') | (F.text.contains('schedule')))
@private_router.message(Command('schedule'))
async def options_cmd(message: types.Message):
    await message.answer('our current schedule')
