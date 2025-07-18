from typing import List, Tuple, Any, Optional, Union
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery  # move

from tg_bot.services.service import get_all_tickers
from tg_bot.config import SETTINGS_OPTIONS, OI_TIMEFRAMES, EXCHANGES, LANGUAGES

from tg_bot.keyboards.inline import NEXT, PREV, MAIN_MENU

from tg_bot.utils import retrieve_data_for_sub_menu


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