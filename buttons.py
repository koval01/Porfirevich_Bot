from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_main_menu.add(KeyboardButton('🎲🎲'))
button_main_menu.add(KeyboardButton('Как добавить свою запись?'))