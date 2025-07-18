from telebot.types import Message, CallbackQuery
from typing import List, Tuple, Any, Optional, Union
from telebot.types import InlineKeyboardMarkup  # move


from tg_bot.loader import bot
from tg_bot.config import SETTINGS_OPTIONS, OI_TIMEFRAMES, EXCHANGES, LANGUAGES

from tg_bot.keyboards.inline import create_settings_keyboard_subgeneral, create_settings_keyboard_general



@bot.message_handler(commands=["settings"])
def handle_settings(message: Message) -> None:
    keyboard = create_settings_keyboard_general(SETTINGS_OPTIONS)
    bot.send_message(chat_id=message.chat.id, text="Main Menu", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in [i[0] for i in SETTINGS_OPTIONS])
def handle_sub_settings(call: CallbackQuery) -> None:
    keyboard_tuple: Tuple[InlineKeyboardMarkup, Optional[str]] = create_settings_keyboard_subgeneral(SETTINGS_OPTIONS, call)
    keyboard = keyboard_tuple[0]
    keyboard_text: str = keyboard_tuple[1] if keyboard_tuple[1] else call.data
    bot.edit_message_text(text=keyboard_text, chat_id=call.message.chat.id, message_id=call.message.id,reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def handle_return_to_main_settings(call: CallbackQuery) -> None:
    keyboard = create_settings_keyboard_general(SETTINGS_OPTIONS)
    bot.edit_message_text(chat_id=call.message.chat.id, text="Main Menu", message_id=call.message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in OI_TIMEFRAMES)
def handle_oi_timeframe_settings(call: CallbackQuery) -> None:
    # keyboard: InlineKeyboardMarkup = 
    pass

