from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

finish_registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='В профиль➡️', callback_data='profile')],
])