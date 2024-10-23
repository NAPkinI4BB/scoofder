import asyncio
from aiogram import Bot, Dispatcher

import handlers.user_handlers
from config.config import BotConfig, load_config


async def main():
    dp = Dispatcher()

    config: BotConfig = load_config()
    bot = Bot(token=config.bot.token)
    dp.include_router(handlers.user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
