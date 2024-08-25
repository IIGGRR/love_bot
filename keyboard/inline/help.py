from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Информация📖', callback_data='help info')],
    [InlineKeyboardButton(text="Сообщить об ошибке✏️", callback_data='help error')],
])

return_main_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад➡️', callback_data='main help returned')]
])