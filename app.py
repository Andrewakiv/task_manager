import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from decouple import config

bot = Bot(token=config('TOKEN'))

dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('this answer for start command')


@dp.message()
async def echo(message: types.Message):
    await message.answer('echo echo')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
