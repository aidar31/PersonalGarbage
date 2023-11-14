import asyncio
import logging
from aiogram import Bot, Dispatcher

from db import Base, engine
from config import TOKEN

from routers import user

async def main():
    Base.metadata.create_all(bind=engine)
    bot = Bot(TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    logging.basicConfig(level=logging.DEBUG)

    dp.include_routers(
        user.router,
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())