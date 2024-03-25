import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from decouple import config
from handlers import private, group, homeworks, games
from optional import options


async def main():
    bot = Bot(token=config('TOKEN'), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(private.private_router, group.group_router, homeworks.homework_router, games.games_router)

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands()
    await bot.set_my_commands(commands=options.private)
    await dp.start_polling(bot)


asyncio.run(main())
