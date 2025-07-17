from telebot.types import Message, CallbackQuery
from typing import List, Tuple, Any, Optional, Union
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # move


from tg_bot.loader import bot
from tg_bot.services.service import get_all_tickers
from tg_bot.config import SETTINGS_OPTIONS, OI_TIMEFRAMES, EXCHANGES, LANGUAGES


NEXT = InlineKeyboardButton(text="Next", callback_data="next")  # (move)
PREV = InlineKeyboardButton(text="Previous", callback_data="prev")  # (move)
MAIN_MENU = InlineKeyboardButton(text="Main Menu", callback_data="main_menu")  # (move)

# (move) function for creating main menu of settings
def create_settings_keyboard_general(settings_list: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()

    for setting in settings_list:
        button: InlineKeyboardButton = InlineKeyboardButton(text=setting[0], callback_data=setting[0])
        keyboard.add(button)
    
    return keyboard


# (move) function of creating sub menu for settings like timeframe, exchange, etc.
def create_settings_keyboard_subgeneral(settings_list: List[Tuple[str, str]], call: CallbackQuery) -> Tuple[InlineKeyboardMarkup, Optional[str]]:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()

    sub_menu_data: Optional[List[str | Tuple[str, str]]] | str = retrieve_data_for_sub_menu(settings_list, call)

    if sub_menu_data is None:
        error_str: str = "Error occured. Please, try something else."
        keyboard.add(MAIN_MENU)
        return keyboard, error_str
    elif type(sub_menu_data) == list:
        sub_menu_data: List[str]
        sub_menu_buttons: List[InlineKeyboardButton] = [InlineKeyboardButton(text=item, callback_data=item) for item in sub_menu_data]
        keyboard.add(*sub_menu_buttons)
        keyboard.add(MAIN_MENU)
    elif type(sub_menu_data) == str:
        keyboard.add(MAIN_MENU)
        return keyboard, sub_menu_data
    elif type(sub_menu_data) == tuple:
        sub_menu_data: List[str] = [setting[0] for setting in settings_data]
        sub_menu_buttons: List[InlineKeyboardButton] = [InlineKeyboardButton(text=item, callback_data=item) for item in sub_menu_data]
        keyboard.add(*sub_menu_buttons)
        keyboard.add(MAIN_MENU)
        

    return (keyboard, None)

# (move) function for handling choice of data for sub menu
def retrieve_data_for_sub_menu(settings_list: List[Tuple[str, str]], call: CallbackQuery) -> Optional[List[str | Tuple[str, str]] | str]:
    sub_menus: List[str] = [setting[0] for setting in settings_list]
    call_data: Optional[str] = call.data

    # check if setting exists
    if call_data not in sub_menus:
        return
    # check if setting is not in development
    if settings_list[sub_menus.index(call_data)][1] == "in development":
        return "Sorry, this segment is in development"
    
    # choose data for retrieval
    if call_data == "Timeframe":
        return OI_TIMEFRAMES
    elif call_data == "Exhange":
        return EXCHANGES
    elif call_data == "Language":
        return LANGUAGES
    elif call_data == "Crypto Symbols":
        all_available_tickers: Optional[List[str]] = get_all_tickers()
        return all_available_tickers


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
    pass
