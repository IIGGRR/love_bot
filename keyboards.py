from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='кНИГА жалоб'),
                                       KeyboardButton(text='люблю тебя')],
                                      [KeyboardButton(text='информация')],
                                      [KeyboardButton(text='кыс')]], resize_keyboard=True)


async def get_photo_keyboard(photos):
    keyboard = InlineKeyboardBuilder()
    for photo in photos:
        keyboard.add(InlineKeyboardButton(text=f'photo {photo.id}', callback_data=f'photo {photo.id}'))
    return keyboard.adjust(2).as_markup()

