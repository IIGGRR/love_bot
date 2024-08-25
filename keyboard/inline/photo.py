from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def start_photo_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить фоточку📸', callback_data='send_photo')],
        [InlineKeyboardButton(text='Галерея🖼', callback_data='all_photo')],
        [InlineKeyboardButton(text='Ваши фото📷', callback_data='my_photos')],
    ])
    return keyboard


async def get_photo_keyboard(photos):
    keyboard = InlineKeyboardBuilder()
    for photo in photos:
        keyboard.add(InlineKeyboardButton(text=f'{photo.name}', callback_data=f'photo {photo.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад◀️', callback_data=f'main photo menu back'))
    return keyboard.adjust(2).as_markup()


async def get_my_photo_keyboard(photos):
    keyboard = InlineKeyboardBuilder()
    for photo in photos:
        keyboard.add(InlineKeyboardButton(text=f'{photo.name}', callback_data=f'my photo {photo.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад◀️', callback_data=f'main photo menu back'))
    return keyboard.adjust(2).as_markup()


async def my_photo_control_keyboard(photo_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Удалить фото🗑', callback_data=f'delete my photo {photo_id}')],
        [InlineKeyboardButton(text='Переименовать✍️', callback_data=f'rename my photo {photo_id}')],
        [InlineKeyboardButton(text='Скинуть в чат партнера😋', callback_data=f'forward my photo {photo_id}')],
        [InlineKeyboardButton(text='Назад◀️', callback_data=f'my_photos back')],
    ])
    return keyboard

back_to_my_photos_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад◀️', callback_data=f'my_photos back')]
])

back_to_photos_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад◀️', callback_data=f'all_photo back')]
])

back_to_main_photo_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад◀️', callback_data=f'main photo menu back')]
])



