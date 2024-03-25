import asyncio
import json

import aiofiles
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.for_navigate import games_keyboard
from filters.type_of_chat import ChatTypeFilter

games_router = Router()
games_router.message.filter(ChatTypeFilter(['private']))


async def read_file():
    async with aiofiles.open('./games.json', encoding='utf-8') as file:
        data = await file.read()
        json_data = json.loads(data)
    return json_data


async def write_file(data):
    async with aiofiles.open('./games.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4))


@games_router.message(Command('games'))
async def homeworks_cmd(message: types.Message):
    await message.answer('Яку дію виконати з іграми?', reply_markup=games_keyboard)


@games_router.message(F.text == 'view all games')
async def all_homeworks_cmd(message: types.Message):
    games_list = await read_file()
    for i in await read_file():
        text = as_marked_section(
            Underline(Bold('Game')),
            as_key_value('Назва ', i['topic']),
            as_key_value('Жанр ', i['number']),
            as_key_value('Студія ', i['content']),
            marker='📌 '
        )
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text='видалити гру', callback_data=f'deletegame_{games_list.index(i)}')
        )

        await message.answer(text.as_html(), reply_markup=builder.as_markup())
        await asyncio.sleep(0.3)


@games_router.callback_query(F.data.split('_')[0] == 'deletegame')
async def del_game(callback: types.CallbackQuery):  # 'delete_1'
    game_id = callback.data.split('_')[-1]
    games_list = await read_file()  # []
    games_list.pop(int(game_id))
    await write_file(games_list)
    await callback.message.answer('Гру видалено!')
    await callback.answer('Its ok, game has been deleted', show_alert=True)


class AddGame(StatesGroup):
    topic = State()
    genre = State()
    studio = State()


@games_router.message(StateFilter(None), F.text == 'add new game')
async def add_homeworks_cmd(message: types.Message, state: FSMContext):
    await message.answer('Введіть назву гри: ', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddGame.topic)


@games_router.message(Command("cancel"))
@games_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@games_router.message(AddGame.topic, F.text)
async def add_number_cmd(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer('Введіть жанр гри: ')
    await state.set_state(AddGame.genre)


@games_router.message(AddGame.genre, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('Введіть студію: ')
    await state.set_state(AddGame.studio)


@games_router.message(AddGame.studio, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer('Гру додано!', reply_markup=games_keyboard)
    data = await state.get_data()
    data_to_update = await read_file()
    data_to_update.append(data)
    await write_file(data_to_update)
    await message.answer(str(data))
    await state.clear()
