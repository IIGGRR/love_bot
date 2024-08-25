from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


add_partner_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить половинку❤️', callback_data='add_partner')],
])

delete_partner_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить половинку💔', callback_data='delete_partner')],
])

confirm_delete_partner_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить🙊', callback_data='confirm delete_partner'), InlineKeyboardButton(text='Назад◀️', callback_data='main_profile cancel delete_partner')],
])

choice_add_partner_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ссылка-приглашение (база)', callback_data='add_partner link')],
    [InlineKeyboardButton(text='Назад◀️', callback_data='main_profile cancel add_partner')],
])

returning_main_profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад◀️', callback_data='main_profile returning')],
])
