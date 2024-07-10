from aiogram import html, F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards import start, get_photo_keyboard
import os
from dotenv import load_dotenv
from databasa.requests import get_id_partner, set_photo, get_photo, get_all_photo_partner, delete_all_photo, get_id

router = Router(name=__name__)
PHOTOS_DIR = "lovebot/photos"

load_dotenv()

admin_id = os.getenv('ADMIN_ID')


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


@router.message(F.text == 'напомнить о любви')
async def skuch_handler(message: Message, bot: Bot):
    await message.answer('Напоминание отправлено')
    #    await message.answer_photo(photo='')
    tg_fr_id_1 = str(await get_id_partner(message.from_user.id))
    await bot.send_message(tg_fr_id_1, text=f'динь от партнёра')


@router.message(F.text == 'получить фотку')
async def love_handler(message: Message) -> None:
    user_fr_id = await get_id_partner(message.from_user.id)
    photos = await get_all_photo_partner(user_fr_id)
    await message.answer('чмок :*')
    await message.answer(text='что то написал', reply_markup=await get_photo_keyboard(photos))


@router.callback_query(F.data.startswith('photo'))
async def send_photo_handler(call: CallbackQuery, bot: Bot):
    photo_id = call.data.split()[-1]
    photo = await get_photo(photo_id)
    photo_file = FSInputFile(photo.file_path)
    print(photo_file)
    print(photo.file_path)
    await bot.send_photo(call.message.chat.id, photo_file)
    await call.answer()


@router.message(F.text == 'отправка фоточки')
async def photo_handler(message: Message):
    await message.answer('отправь фотку, быстро!')


@router.message(F.text == 'Сообщить об ошибке')
async def sign_handler(message: Message):
    await message.answer("напиши об ошибке. начни сообщение так - 'Сообщение:'")


@router.message(F.text.startswith('Сообщение:'))
async def sign_repeat_handler(message: Message, bot: Bot):
    await message.answer('Сообщение отправлено')
    try:
        await bot.send_message(admin_id, text=f'{message.text}. {message.from_user.full_name}')
    except:
        await bot.send_message(admin_id, text=message.text)


@router.message(F.photo)
async def add_photo_handler(message: Message, bot: Bot):
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
    tg_id = message.from_user.id
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = os.path.join(PHOTOS_DIR, file_info.file_unique_id + '.jpg')
    print(file_path)
    await bot.download(photo, file_info.file_unique_id)
    user_id = await get_id(tg_id)
    await set_photo(file_path=file_path, user_id=user_id)
    await message.answer(text='принято')
    tg_fr_id_1 = str(await get_id_partner(message.from_user.id))
    await bot.send_message(tg_fr_id_1, text=f'фотка от партнёра')


@router.startup()
async def on_startup(bot: Bot):
    from commands import set_commands
    await set_commands(bot)
    await bot.send_message(admin_id, text=f'<tg-spoiler>Начало работы</tg-spoiler>')


@router.shutdown()
async def on_shutdown(bot: Bot):
    await bot.send_message(admin_id, text=f'<tg-spoiler>КОНЕЦ!</tg-spoiler>')
