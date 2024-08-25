import re

from aiogram import Router, Bot, html
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.utils.payload import decode_payload
from love_bot.database.requests.user import get_user_by_tg_id, set_user, add_sync_tg_fr_id
from love_bot.keyboard.reply.start import start

router = Router(name=__name__)


class RegistrationForm(StatesGroup):
    tg_id = State()
    message_id = State()
    ancillary_message_id = State()
    tg_partner_id = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot, command: CommandObject, state: FSMContext) -> None:
    await state.clear()
    args = command.args
    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)
    if user is None:
        username = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ\s]', '', message.from_user.full_name)
        await message.answer(f"Добро пожаловать, {html.bold(username)}!")
        if args:
            reference = decode_payload(args)
            partner = await get_user_by_tg_id(reference)
            ancillary_message = await message.answer(f"Ваша половинка {partner.name}")
            await state.update_data(tg_partner_id=reference)
            await state.update_data(ancillary_message_id=ancillary_message.message_id)
        answer = await message.answer(text='Как к вам обращаться?🙈\n')
        await state.set_state(RegistrationForm.tg_id)
        await state.update_data(tg_id=tg_id)
        await state.update_data(message_id=answer.message_id)
    else:
        if args:
            if user.tg_fr_id is None:
                tg_fr_id = decode_payload(args)
                await add_sync_tg_fr_id(tg_id, tg_fr_id)
                partner = await get_user_by_tg_id(tg_fr_id)
                await message.answer(f'Половинка {partner.name} добавлена!❤️', reply_markup=start)
            else:
                await message.answer('У вас уже есть половинка!✅\n Подробнее у профиле🙊', reply_markup=start)
        else:
            await message.answer(f"С возвращением, {user.name}!❤️", reply_markup=start)
        await state.clear()


@router.message(RegistrationForm.tg_id)
async def finish_registration_handler(message: Message, state: FSMContext, bot: Bot):
    context = await state.get_data()
    message_id = context.get('message_id')
    ancillary_message_id = context.get('ancillary_message_id')
    tg_partner_id = context.get('tg_partner_id')
    tg_id = context.get('tg_id')
    name = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    if ancillary_message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=ancillary_message_id)
    await set_user(tg_id=tg_id, name=name, tg_fr_id=tg_partner_id)
    if tg_partner_id is None:
        await message.answer(text=f'Вы успешно зарегистрировались😇\n '
                                  f'{html.bold('Добавьте свою половинку в профиле')}', reply_markup=start)
    else:
        await message.answer(text=f'Вы успешно зарегистрировались😇', reply_markup=start)
    await state.clear()







