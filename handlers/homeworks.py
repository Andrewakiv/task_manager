from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.for_navigate import homeworks_keyboard
from filters.type_of_chat import ChatTypeFilter

homework_router = Router()
homework_router.message.filter(ChatTypeFilter(['private']))


@homework_router.message(Command('homeworks'))
async def homeworks_cmd(message: types.Message):
    await message.answer('Яку дію виконати з дз?', reply_markup=homeworks_keyboard)


@homework_router.message(F.text == 'view all homeworks')
async def all_homeworks_cmd(message: types.Message):
    await message.answer('check all')


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
    await message.answer(str(data))
    await state.clear()
