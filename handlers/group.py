from aiogram import Router, types
from aiogram.filters import Command

group_router = Router()


@group_router.message(Command('group'))
async def options_cmd(message: types.Message):
    await message.answer('group command')
