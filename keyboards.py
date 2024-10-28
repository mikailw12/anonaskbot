from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancelkb = InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text='Отменить ❌', callback_data='cancel')]
])