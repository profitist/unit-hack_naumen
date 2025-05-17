from dotenv import load_dotenv
import os
import asyncio
from aiogram import Bot, Dispatcher
from app.handlers.handlers import register_all_handlers
from database.session import init_db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
register_all_handlers(dp)


async def main():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Exit")
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())
