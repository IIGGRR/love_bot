from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from love_bot.databasa import set_user, check_registration


router = Router(name=__name__)


class RegistrationForm(StatesGroup):
    tg_id = State()


@router.message(Command('registration'))
async def reg(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    if await check_registration(tg_id):
        await state.set_state(RegistrationForm.tg_id)
        await state.update_data(tg_id=tg_id)
        await message.answer(text='Пришли ID своей/своего зайки/волчары. Его можно получить в боте https://t.me/getmyid_bot')
    else:
        await message.answer(text='ВЫ уже зарегистрированы, выйди отсюда, разбийник')


@router.message(RegistrationForm.tg_id)
async def final_reg(message: Message, state: FSMContext):
    tg_fr_id = message.text
    context = await state.get_data()
    tg_id = context['tg_id']
    await set_user(tg_id, tg_fr_id)
    await message.answer(text='успешно зарегистрированы!')


