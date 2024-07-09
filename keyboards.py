from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='кНИГА жалоб'),
                                       KeyboardButton(text='информация')],
                                      [KeyboardButton(text='получить фотку'),
                                       KeyboardButton(text='отправка фоточки')],
                                      [KeyboardButton(text='напомнить о любви'),
                                      KeyboardButton(text='Сообщить об ошибке')]], resize_keyboard=True)


async def get_photo_keyboard(photos):
    keyboard = InlineKeyboardBuilder()
    for photo in photos:
        keyboard.add(InlineKeyboardButton(text=f'photo {photo.id}', callback_data=f'photo {photo.id}'))
    return keyboard.adjust(2).as_markup()

