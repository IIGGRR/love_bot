from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_roleplay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Позвать половинку', callback_data='roleplay call partner')]
])

return_main_roleplay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад➡️', callback_data='returned roleplay main menu')],
])