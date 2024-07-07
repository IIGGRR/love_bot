import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from databasa.models import async_main

dp = Dispatcher()


async def main() -> None:
    await async_main()
    bot = Bot(token='7312772482:AAGde65w8x-WQ7BmR-3xnq4-7H3d3VQbnGQ', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    from handlers import router
    dp.include_router(router)
    from registration import router
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
