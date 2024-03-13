from aiogram import Router, types
from aiogram.filters import Command

from filters.type_of_chat import ChatTypeFilter

group_router = Router()
group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))


@group_router.message(Command('group'))
async def options_cmd(message: types.Message):
    await message.answer('group command')
