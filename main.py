import asyncio
from aiogram import Bot, Dispatcher

import handlers.user_handlers
import handlers.newform_fsm
from config.config import BotConfig, load_config
from database.connectDB_class import ConnectDB

config: BotConfig = load_config()
bot = Bot(token=config.bot.token)

dbase = ConnectDB()

dp = Dispatcher(bot=bot)

dp.include_router(handlers.user_handlers.router)
dp.include_router(handlers.newform_fsm.router)

dp['db'] = dbase


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
