from aiogram import Router, Bot
import os
from dotenv import load_dotenv


import re

router = Router(name=__name__)
PHOTOS_DIR = "photos"

load_dotenv()

admin_id = os.getenv('ADMIN_ID')


@router.startup()
async def on_startup(bot: Bot):
    from love_bot.core.commands import set_commands
    await set_commands(bot)
    await bot.send_message(admin_id, text=f'<tg-spoiler>Начало работы</tg-spoiler>')


@router.shutdown()
async def on_shutdown(bot: Bot):
    await bot.send_message(admin_id, text=f'<tg-spoiler>КОНЕЦ!</tg-spoiler>')
