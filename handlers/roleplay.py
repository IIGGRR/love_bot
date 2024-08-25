import html

from aiogram import F, Router, Bot
from aiogram.utils.markdown import hlink
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
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
from love_bot.keyboard.inline.roleplay import main_roleplay_keyboard, return_main_roleplay_keyboard


router = Router(name=__name__)


@router.message(F.text.startswith('RP с партнёром'))
async def main_roleplay_handler(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text='<b>Добро пожаловать в меню взаимодействий c вашей половинкой</b>🥹\n'
                              'Выберите кнопку:', parse_mode='HTML', reply_markup=main_roleplay_keyboard)


@router.callback_query(F.data.startswith('roleplay call partner'))
async def call_partner_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    tg_id = call.from_user.id
    partner = await get_tg_id_partner(tg_id)
    await bot.send_message(chat_id=partner, text='Ваша половинка зовет вас!🥹')
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Послание отправлено!👌', reply_markup=return_main_roleplay_keyboard)


@router.callback_query(F.data.startswith('returned roleplay main menu'))
async def returned_main_menu_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>Добро пожаловать в меню взаимодействий c вашей половинкой</b>🥹\n'
                                     'Выберите кнопку:', parse_mode='HTML', reply_markup=main_roleplay_keyboard
                                )