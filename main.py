from dotenv import load_dotenv
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.handlers import set_commands


from database.session import init_db

logging.basicConfig(level=logging.INFO)
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)
    try:
        await set_commands(bot)
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Exit")
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())