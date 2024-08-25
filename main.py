import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

dp = Dispatcher()

dot = load_dotenv('.env')

API_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    # wait async_main()
    # await add_visits()
    from handlers.basic import router as basic_router
    dp.include_router(basic_router)
    from handlers.help_handler import router as help_router
    dp.include_router(help_router)
    from handlers.photo import router as photo_router
    dp.include_router(photo_router)
    from handlers.registration import router as registration_router
    dp.include_router(registration_router)
    from handlers.profile import router as profile_router
    dp.include_router(profile_router)
    from handlers.roleplay import router as roleplay_router
    dp.include_router(roleplay_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
