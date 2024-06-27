from aiogram import html, F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import start
from random import choice
router = Router(name=__name__)

spisok = []


spisok_2 = []

admin_id = '6494107709'


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    try:
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=start)
    except:
        await message.answer(f"Hello!", reply_markup=start)


@router.message(F.text == 'кНИГА жалоб')
async def fuck_handler(message: Message) -> None:
    await message.answer('ухади рассист, фу!')
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEGX_xmeIEkexAlIEoB55tNgEYksRTlaAACYT8AAiAkKUkqrZaBEfvGjTUE')


@router.message(F.text == 'информация')
async def info_handler(message: Message) -> None:
    await message.answer('Сам ничего не знаю, приходите позднее...')
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEGX_pmeIDxvHA-GK_Lk-zC-WlH_FhZyQACS0kAAnyuIUlbyMk3INlkjDUE')


@router.message(F.sticker)
async def get_sticker_handler(message: Message):
    id_stic = message.sticker.file_id
    print(id_stic)
    await message.answer_sticker(sticker=id_stic)


@router.message(F.text == 'кыс')
async def skuch_handler(message: Message, bot: Bot):
    await message.answer('Напоминание отправлено')
#    await message.answer_photo(photo='')
    await bot.send_message(admin_id, text=f'динь от "{message.from_user.full_name}"')


@router.message(F.text == 'люблю тебя')
async def love_handler(message: Message) -> None:
    await message.answer('и я тебя:) чмок')
    await message.answer_photo(photo=choice(spisok_2))


@router.message(F.photo)
async def photo_handler(message: Message):
    spisok_2.append(str(message.photo[-1].file_id))
    await message.answer(f'ID photo: {message.photo[-1].file_id}')


@router.startup()
async def on_startup(bot: Bot):
    from love_bot.commands import set_commands
    await set_commands(bot)
    await bot.send_message(admin_id, text=f'<tg-spoiler>Начало работы</tg-spoiler>')


@router.shutdown()
async def on_shutdown(bot: Bot):
    await bot.send_message(admin_id, text=f'<tg-spoiler>КОНЕЦ!</tg-spoiler>')
