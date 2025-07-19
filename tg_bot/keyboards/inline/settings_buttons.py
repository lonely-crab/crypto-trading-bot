from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

NEXT = InlineKeyboardButton(text="Next", callback_data="next")
PREV = InlineKeyboardButton(text="Previous", callback_data="prev")
MAIN_MENU = InlineKeyboardButton(text="Main Menu", callback_data="main_menu")
SELECT_ALL = InlineKeyboardButton(text="Select all", callback_data="select_all")
UNSELECT_ALL = InlineKeyboardButton(text="Unselect all", callback_data="unselect_all")
