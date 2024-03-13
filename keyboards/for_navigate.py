from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# keyboard = types.ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             types.KeyboardButton(text='options'),
#             types.KeyboardButton(text='schedule'),
#         ],
#         [
#             types.KeyboardButton(text='links'),
#             types.KeyboardButton(text='homeworks'),
#         ],
#         [
#             types.KeyboardButton(text='about'),
#         ]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder='Choose your command'
# )

keyboard = ReplyKeyboardBuilder()
keyboard.add(
    types.KeyboardButton(text='options'),
    types.KeyboardButton(text='schedule'),
    types.KeyboardButton(text='links'),
    types.KeyboardButton(text='homeworks'),
    types.KeyboardButton(text='about'),
)
keyboard.adjust(3, 2)
