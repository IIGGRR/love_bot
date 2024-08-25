from aiogram import F, Router, Bot
from aiogram.utils.markdown import hlink
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from love_bot.utils.cloudinary import cloudinary as cloudi
from love_bot.keyboard.inline.photo import (get_photo_keyboard, start_photo_keyboard, get_my_photo_keyboard,
                                            my_photo_control_keyboard, back_to_my_photos_keyboard,
                                            back_to_main_photo_menu_keyboard)
from love_bot.keyboard.inline.profile import add_partner_keyboard, choice_add_partner_keyboard, returning_main_profile_keyboard, delete_partner_keyboard, confirm_delete_partner_keyboard
import os
from love_bot.database.requests.photo import set_photo, get_photo, get_all_photos_partner, get_my_photo, delete_my_photo, rename_my_photo
from love_bot.database.requests.user import get_id, get_tg_id_partner, get_user_by_tg_id, get_partner, delete_partner
from aiogram.utils.deep_linking import create_start_link, create_deep_link, create_telegram_link
from aiogram.fsm.state import State, StatesGroup
from love_bot.keyboard.inline.help import main_help_keyboard, return_main_help_keyboard


router = Router(name=__name__)
load_dotenv()
admin_id = os.getenv('ADMIN_ID')


class ErrorForm(StatesGroup):
    text = State()
    message_id = State()

@router.message(F.text.startswith('Помощь'))
async def main_help_handler(message: Message, state: FSMContext, bot: Bot):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer('Это панель помощи🤗\n'
                         'Выберите кнопку:', reply_markup=main_help_keyboard)


@router.message(F.text == 'кНИГА жалоб')
async def fuck_handler(message: Message) -> None:
    await message.answer('ухади рассист, фу!')
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEGX_xmeIEkexAlIEoB55tNgEYksRTlaAACYT8AAiAkKUkqrZaBEfvGjTUE')


@router.callback_query(F.data.startswith('help error'))
async def help_error_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    answer = await bot.edit_message_text(text="Опишите подробно свою проблему. \nадминистратор в скором времени вам ответит❤️",
                                         chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.set_state(ErrorForm.text)
    await state.update_data(message_id=answer.message_id)


@router.message(ErrorForm.text)
async def sign_repeat_handler(message: Message, bot: Bot, state: FSMContext):
    text = message.text
    context = await state.get_data()
    message_id = context.get('message_id')
    await bot.edit_message_text(text='Ваше письмо отправлено✅', message_id=message_id,
                                chat_id=message.chat.id, reply_markup=return_main_help_keyboard)
    await bot.send_message(chat_id=admin_id, text=text)
    await state.clear()


@router.message(F.sticker)
async def get_sticker_handler(message: Message):
    id_stic = message.sticker.file_id
    await message.answer_sticker(sticker=id_stic)


@router.callback_query(F.data.startswith('main help'))
async def main_help_returned_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await bot.edit_message_text(text='Это панель помощи🤗\nВыберите кнопку:', reply_markup=main_help_keyboard,
                                chat_id=call.message.chat.id, message_id=call.message.message_id)
