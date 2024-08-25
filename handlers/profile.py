
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from love_bot.keyboard.inline.profile import add_partner_keyboard, choice_add_partner_keyboard, returning_main_profile_keyboard, delete_partner_keyboard, confirm_delete_partner_keyboard

from love_bot.database.requests.user import get_user_by_tg_id, delete_partner, get_tg_id_partner
from aiogram.utils.deep_linking import create_start_link
from aiogram.fsm.state import State, StatesGroup


router = Router(name=__name__)


@router.message(F.text.startswith('Профиль'))
async def main_profile_handler(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)
    partner = await get_user_by_tg_id(user.tg_fr_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if partner is not None:
        await message.answer(
            text=f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖ \n'
                f'📊Личная информация: \n\n'
                f'🅰️Имя: {user.name} \n'
                f'❤️Ваша половинка: {partner.name} \n'
                f'📆Аккаунт создан: {user.reg_date.strftime("%Y-%m-%d %H:%M")} \n'
                f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖',
                             parse_mode='HTML', reply_markup=delete_partner_keyboard)
    else:
        await message.answer(
            text=f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖ \n'
                 f'📊Личная информация: \n\n'
                 f'🅰️Имя: {user.name} \n'
                 f'📆Аккаунт создан: {user.reg_date.strftime("%Y-%m-%d %H:%M")} \n'
                 f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖ \n\n'
                 f''
                 f'<b>У вас еще нет половинки\n '
                 f'Самое время добавить🙊⬇️</b>',
            parse_mode='HTML', reply_markup=add_partner_keyboard)


@router.callback_query(F.data == 'add_partner')
async def add_partner_handler(call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.edit_message_text(text='Выберите способ:', reply_markup=choice_add_partner_keyboard,
                                chat_id=call.message.chat.id, message_id=call.message.message_id)


@router.callback_query(F.data == 'add_partner link')
async def add_partner_link_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    tg_id = call.from_user.id
    link = await create_start_link(payload=str(tg_id), encode=True, bot=bot)
    await bot.edit_message_text(f"Ваша ссылка-приглашение {link}"
                                f"\n отправьте ее своей половинке❤️",
                                chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=returning_main_profile_keyboard)


@router.callback_query(F.data.startswith('main_profile'))
async def returning_main_profile_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    tg_id = call.from_user.id
    user = await get_user_by_tg_id(tg_id)
    partner = await get_user_by_tg_id(user.tg_fr_id)
    if partner is not None:
        await bot.edit_message_text(
            text=f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖ \n'
                f'📊Личная информация: \n\n'
                f'🅰️Имя: {user.name} \n'
                f'❤️Ваша половинка: {partner.name} \n'
                f'📆Аккаунт создан: {user.reg_date.strftime("%Y-%m-%d %H:%M")} \n'
                f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖',
                             parse_mode='HTML', reply_markup=delete_partner_keyboard,
                             chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        await bot.edit_message_text(
            text=f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖ \n'
                 f'📊Личная информация: \n\n'
                 f'🅰️Имя: {user.name} \n'
                 f'📆Аккаунт создан: {user.reg_date.strftime("%Y-%m-%d %H:%M")} \n'
                 f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖ \n\n'
                 f''
                 f'<b>У вас еще нет половинки\n '
                 f'Самое время добавить🙊⬇️</b>',
            parse_mode='HTML', reply_markup=add_partner_keyboard,
                             chat_id=call.message.chat.id, message_id=call.message.message_id)


@router.callback_query(F.data.startswith('delete_partner'))
async def start_delete_partner_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text='Вы уверены?', reply_markup=confirm_delete_partner_keyboard,
                                chat_id=call.message.chat.id, message_id=call.message.message_id)


@router.callback_query(F.data.startswith('confirm delete_partner'))
async def delete_partner_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    tg_id = call.from_user.id
    partner_tg_id = await get_tg_id_partner(tg_id)
    await delete_partner(tg_id)
    user = await get_user_by_tg_id(tg_id)
    await bot.edit_message_text(text='Партнер удален успешно✅', reply_markup=returning_main_profile_keyboard,
                                chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=partner_tg_id, text=f'{user.name} удалил половинку😭💔')

