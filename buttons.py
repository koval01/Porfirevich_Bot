from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_main_menu.add(KeyboardButton('🎲🎲'))
button_main_menu.add(KeyboardButton('Как добавить свою запись?'))


def create_inline_buttons(*button) -> str:
    """Функция генерации Inline кнопок"""

    array_button = []
    global_array_buttons = []

    for i in button:
        array_button = []
        array_button.append(i)
        global_array_buttons.append(array_button)

    result = dict(inline_keyboard=global_array_buttons)

    return result