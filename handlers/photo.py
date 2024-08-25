from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from love_bot.utils.cloudinary import cloudinary as cloudi
from love_bot.keyboard.inline.photo import (get_photo_keyboard, start_photo_keyboard, get_my_photo_keyboard,
                                            my_photo_control_keyboard, back_to_my_photos_keyboard,
                                            back_to_main_photo_menu_keyboard, back_to_photos_keyboard)
import os
from love_bot.database.requests.photo import set_photo, get_photo, get_all_photos_partner, get_my_photo, \
    delete_my_photo, rename_my_photo
from love_bot.database.requests.user import get_id, get_tg_id_partner

from aiogram.fsm.state import State, StatesGroup

router = Router(name=__name__)
PHOTOS_DIR = "photos"


class UserForm(StatesGroup):
    user_id = State()
    tg_id = State()
    tg_partner_id = State()
    send_photo = State()
    name_photo = State()
    photo_id = State()
    message_id = State()


@router.message(F.text.startswith('Фотки!'))
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Выберите кнопку:', reply_markup=await start_photo_keyboard())
    tg_id = message.from_user.id
    await state.update_data(tg_id=tg_id)
    user_id = await get_id(tg_id)
    await state.update_data(user_id=user_id)
    tg_partner_id = await get_tg_id_partner(tg_id)
    await state.update_data(tg_partner_id=tg_partner_id)


@router.callback_query(F.data.startswith('all_photo'))
async def get_all_photo_handler(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    #await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    context = await state.get_data()
    tg_partner_id = context['tg_partner_id']
    partner_id = await get_id(tg_partner_id)
    photos = await get_all_photos_partner(partner_id)
    if photos is not None:
        await bot.edit_message_text(text='Галерея фото вашего партнёра😇', reply_markup=await get_photo_keyboard(photos),
                                    chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        await bot.edit_message_text(text='Тут пока-что пусто, ждите фоточки от партнёра😇', chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)
    await call.answer()


@router.callback_query(F.data.startswith('photo'))
async def get_photo_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    photo_id = call.data.split()[-1]
    photo = await get_photo(photo_id)
    """ photo_file = FSInputFile(photo.file_path)
    await bot.send_photo(call.message.chat.id, photo_file)
    await call.answer()"""
    await call.message.answer_photo(photo.file_path)
    await call.message.answer(text='Вернуться', reply_markup=back_to_photos_keyboard)
    await call.answer()


@router.callback_query(F.data == 'send_photo')
async def add_name_photo_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    #await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    answer = await bot.edit_message_text(text='Введите название фотографии😌\nограничение 32 символа',
                                         reply_markup=back_to_main_photo_menu_keyboard,
                                         chat_id=call.message.chat.id,
                                         message_id=call.message.message_id)
    await state.set_state(UserForm.send_photo)
    await state.update_data(message_id=answer.message_id)
    await call.answer()


@router.message(UserForm.send_photo)
async def send_photo_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    context = await state.get_data()
    message_id = context['message_id']
    # await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.update_data(name_photo=message.text[:31])
    answer = await bot.edit_message_text(text='Отправь фоточку☺️', chat_id=message.chat.id, message_id=message_id)
    await state.set_state(UserForm.name_photo)
    await state.update_data(message_id=answer.message_id)


@router.message(UserForm.name_photo)
async def add_photo_handler(message: Message, bot: Bot, state: FSMContext):
    context = await state.get_data()
    message_id = context['message_id']
    user_id = context['user_id']
    tg_id = context['tg_id']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.update_data(message_id=None)
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
    context = await state.get_data()
    photo = message.photo[-1]
    name_photo = context.get('name_photo')
    file_info = await bot.get_file(photo.file_id)
    file_path = os.path.join(PHOTOS_DIR, file_info.file_unique_id + '.jpg')
    await bot.download(photo, file_path)
    photo_url = None
    public_id = None
    with open(file_path, 'rb') as f:

        result = cloudi.uploader.upload(f)
        photo_url = result.get('secure_url')
        public_id = result.get('public_id')
    if photo_url:

        await set_photo(file_path=photo_url, user_id=user_id, name=name_photo, public_id=public_id)
        await message.answer(text='принято', reply_markup=back_to_main_photo_menu_keyboard)
    else:
        await message.answer(text='ошибка', reply_markup=back_to_main_photo_menu_keyboard)
    os.remove(file_path)
    '''if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
    file_path = os.path.join(PHOTOS_DIR, file_info.file_unique_id + '.jpg')

    await bot.download(photo, file_path)
    user_id = await get_id(tg_id)
    await set_photo(file_path=file_path, user_id=user_id)
    await message.answer(text='принято')
    '''
    tg_partner_id = context['tg_partner_id']
    await bot.send_message(tg_partner_id, text=f'фотка от партнёра')
    await state.clear()
    await state.update_data(tg_id=tg_id)


@router.callback_query(F.data.startswith('my_photos'))
async def get_my_photos_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    context = await state.get_data()
    user_id = context.get('user_id')
    my_photos = await get_my_photo(user_id)
    if type(context.get('message_id')) == dict:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=context.get('message_id')['photo_answer'])
    if my_photos:
        await bot.edit_message_text(text='Управление вашими фото', reply_markup=await get_my_photo_keyboard(my_photos),
                                    chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        await bot.edit_message_text(text='Тут пока-что пусто, пришлите фоточку партнёру😇',
                                    chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.answer()


@router.callback_query(F.data.startswith('my photo'))
async def get_one_my_photo_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    answers = {}
    photo_id = call.data.split()[-1]
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.update_data(photo_id=photo_id)
    photo = await get_photo(photo_id)
    """ photo_file = FSInputFile(photo.file_path)
    await bot.send_photo(call.message.chat.id, photo_file)
    await call.answer()"""
    photo_answer = await call.message.answer_photo(photo.file_path)
    answer = await call.message.answer(text='Панель управления', reply_markup=await my_photo_control_keyboard(photo_id))
    answers['photo_answer'] = photo_answer.message_id
    answers['answer'] = answer.message_id
    await state.update_data(message_id=answers)
    await call.answer()


@router.callback_query(F.data.startswith('delete my photo'))
async def delete_my_photo_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    photo_id = call.data.split()[-1]
    context = await state.get_data()
    messages = context['message_id']
    await bot.delete_message(chat_id=call.message.chat.id, message_id=messages['photo_answer'])
    photo = await get_photo(photo_id)
    #await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    delete_res = cloudi.uploader.destroy(photo.public_id)
    if delete_res.get('result') == 'ok':
        await delete_my_photo(photo_id)
        await bot.edit_message_text(text='Фото успешно удалена✅', reply_markup=back_to_my_photos_keyboard,
                                    chat_id=call.message.chat.id, message_id=call.message.message_id)

    else:
        await bot.edit_message_text(text='Ошибка удаления, попробуйте снова или обратитесь в поддержку❤️',
                                    reply_markup=back_to_my_photos_keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.update_data(photo_id=None, message_id=messages['answer'])
    await call.answer()


@router.callback_query(F.data.startswith('rename my photo'))
async def rename_my_photo_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    context = await state.get_data()
    messages = context['message_id']
    # await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=messages['photo_answer'])
    answer = await bot.edit_message_text(text='Введите новое название фото',
                                         chat_id=call.message.chat.id, message_id=messages['answer'])
    await state.set_state(UserForm.photo_id)
    await state.update_data(message_id=answer.message_id)
    await call.answer()


@router.message(UserForm.photo_id)
async def end_rename_my_photo_handler(message: Message, bot: Bot, state: FSMContext):
    context = await state.get_data()
    message_id = context.get('message_id')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    new_name = message.text[:31]
    context = await state.get_data()
    photo_id = context['photo_id']
    await rename_my_photo(photo_id, new_name)
    await bot.edit_message_text('Фотография успешно переименована✅', reply_markup=back_to_my_photos_keyboard,
                                chat_id=message.chat.id, message_id=message_id)


@router.callback_query(F.data.startswith('forward my photo'))
async def forward_my_photo_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    context = await state.get_data()
    messages = context['message_id']
    await bot.delete_message(chat_id=call.message.chat.id, message_id=messages['photo_answer'])
    # await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    photo_id = context['photo_id']
    photo = await get_photo(photo_id)
    tg_partner_id = context['tg_partner_id']
    await state.update_data(photo_id=None, message_id=messages['answer'])

    await bot.send_photo(chat_id=tg_partner_id, photo=photo.file_path, caption=f'{photo.name}')
    await bot.edit_message_text(text='Экспресс фотка отправлена✅', reply_markup=back_to_my_photos_keyboard,
                                chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.answer()


@router.callback_query(F.data.startswith('main photo menu back'))
async def return_to_main_menu_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    context = await state.get_data()
    tg_id = context.get('tg_id')
    if context.get('user_id') is None or context.get('tg_partner_id') is None:
        user_id = await get_id(tg_id)
        await state.update_data(user_id=user_id)
        tg_partner_id = await get_tg_id_partner(tg_id)
        await state.update_data(tg_partner_id=tg_partner_id)

    await bot.edit_message_text('Выберите кнопку:', reply_markup=await start_photo_keyboard(),
                                chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.answer()
