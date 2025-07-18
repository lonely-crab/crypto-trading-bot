from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # move

NEXT = InlineKeyboardButton(text="Next", callback_data="next")  # (move)
PREV = InlineKeyboardButton(text="Previous", callback_data="prev")  # (move)
MAIN_MENU = InlineKeyboardButton(text="Main Menu", callback_data="main_menu")  # (move)