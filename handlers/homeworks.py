import asyncio
import json

import aiofiles
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.for_navigate import homeworks_keyboard
from filters.type_of_chat import ChatTypeFilter

homework_router = Router()
homework_router.message.filter(ChatTypeFilter(['private']))


# @homework_router.message(Command('testkb'))
# async def kb_cmd(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="видалити дз",
#         callback_data="delete_value")
#     )
#     await message.answer(
#         "test message",
#         reply_markup=builder.as_markup()
#     )
#
#
# @homework_router.callback_query(F.data == "delete_value")
# async def send_value(callback: types.CallbackQuery):
#     await callback.message.answer('test completed')


async def read_file():
    async with aiofiles.open('./data.json', encoding='utf-8') as file:
        data = await file.read()
        json_data = json.loads(data)
    return json_data


async def write_file(data):
    async with aiofiles.open('./data.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4))


@homework_router.message(Command('homeworks'))
async def homeworks_cmd(message: types.Message):
    await message.answer('Яку дію виконати з дз?', reply_markup=homeworks_keyboard)


@homework_router.message(F.text == 'view all homeworks')
async def all_homeworks_cmd(message: types.Message):
    homeworks_list = await read_file()
    for i in await read_file():
        text = as_marked_section(
            Underline(Bold('Task')),
            as_key_value('Тема ', i['topic']),
            as_key_value('Номер уроку ', i['number']),
            as_key_value('Завдання ', i['content']),
            marker='📌 '
        )
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text='видалити дз', callback_data=f'delete_{homeworks_list.index(i)}')
        )

        await message.answer(text.as_html(), reply_markup=builder.as_markup())
        await asyncio.sleep(0.3)


@homework_router.callback_query(F.data.split('_')[0] == 'delete')
async def del_homework(callback: types.CallbackQuery):  # 'delete_1'
    homework_id = callback.data.split('_')[-1]
    homeworks_list = await read_file()  # []
    homeworks_list.pop(int(homework_id))
    await write_file(homeworks_list)
    await callback.message.answer('Домашню роботу видалено!')
    await callback.answer('Its ok, homework has been deleted', show_alert=True)


class AddHomework(StatesGroup):
    topic = State()
    number = State()
    content = State()


@homework_router.message(StateFilter(None), F.text == 'add new homework')
async def add_homeworks_cmd(message: types.Message, state: FSMContext):
    await message.answer('Введіть тему уроку: ', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddHomework.topic)


@homework_router.message(Command("cancel"))
@homework_router.message(F.text.casefold() == "cancel")
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


@homework_router.message(AddHomework.topic, F.text)
async def add_number_cmd(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer('Введіть номер уроку (1 чи 2): ')
    await state.set_state(AddHomework.number)


@homework_router.message(AddHomework.number, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('Введіть завдання: ')
    await state.set_state(AddHomework.content)


@homework_router.message(AddHomework.content, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer('Завдання додано!', reply_markup=homeworks_keyboard)
    data = await state.get_data()
    data_to_update = await read_file()
    data_to_update.append(data)
    await write_file(data_to_update)
    await message.answer(str(data))
    await state.clear()
