from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f

from filters.type_of_chat import ChatTypeFilter

private_router = Router()
private_router.message.filter(ChatTypeFilter(['private']))


@private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('this answer for start command')


@private_router.message(Command('options'))
async def options_cmd(message: types.Message):
    print(message)
    await message.answer('options list')


@private_router.message(Command('about'))
async def options_cmd(message: types.Message):
    await message.answer('info about bot')


@private_router.message(Command('homeworks'))
async def options_cmd(message: types.Message):
    await message.answer('all homeworks')


@private_router.message(or_f(Command('links'), F.text.lower() == 'посилання'))
async def options_cmd(message: types.Message):
    await message.answer('active links')


@private_router.message((F.text.lower() == 'розклад') | (F.text.contains('schedule')))
@private_router.message(Command('schedule'))
async def options_cmd(message: types.Message):
    await message.answer('our current schedule')
