from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# СОЗДАДИМ ШАБЛОН КЛАВИАТУРЫ
kb_main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# СОЗДАДИМ КНОПКИ ДЛЯ КЛАВИАТУРЫ
btn_help = KeyboardButton('/help')
btn_rules = KeyboardButton('/rules')

# ЗАКРЕПИМ КНОПКИ НА КЛАВИАТУРЕ
kb_main_menu.add(btn_help, btn_rules)