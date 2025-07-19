from typing import List, Tuple, Any, Optional, Union
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery  # move

from tg_bot.services.service import get_all_tickers
from tg_bot.config import SETTINGS_OPTIONS, OI_TIMEFRAMES, EXCHANGES, LANGUAGES

from tg_bot.keyboards.inline import NEXT, PREV, MAIN_MENU, SELECT_ALL, UNSELECT_ALL

from tg_bot.utils import retrieve_data_for_sub_menu

from database.models import session, Users


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

    sub_menu_data: Optional[List[str]] | str = retrieve_data_for_sub_menu(settings_list, call)

    if sub_menu_data is None:
        error_str: str = "Error occured. Please, try something else."
        keyboard.add(MAIN_MENU)
        return keyboard, error_str
    elif type(sub_menu_data) == str:
        keyboard.add(MAIN_MENU)
        return keyboard, sub_menu_data
    elif type(sub_menu_data) == list:
        if len(sub_menu_data) < 30:
            sub_menu_data: List[str]
            sub_menu_buttons: List[InlineKeyboardButton] = [InlineKeyboardButton(text=item, callback_data=item) for item in sub_menu_data]
            keyboard.add(*sub_menu_buttons)
            keyboard.add(MAIN_MENU)

    return (keyboard, None)


def create_symbols_keyboard(settings_list: List[Tuple[str, str]], call: CallbackQuery) -> Tuple[InlineKeyboardMarkup, Optional[str]]:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()

    sub_menu_data: Optional[List[str]| str] = retrieve_data_for_sub_menu(settings_list, call)
    len_symbol_list: int = len(sub_menu_data)

    call_data: Optional[str] = call.data
    username: str = call.from_user.username
    user: Users = session.query(Users).filter(Users.name == username).one()

    if call_data == "Crypto Symbols":
        user.page = 0
    elif call_data == NEXT.callback_data:
        user.page += 1
    elif call_data == PREV.callback_data:
        user.page -= 1
    
    session.commit()

    page: int = user.page
    remainder: int = 1 if len_symbol_list % 30 else 0
    final_page: int = len_symbol_list // 30 + remainder
    
    for i in range(page * 30, min((page + 1) * 30, len_symbol_list), 3):
        sub_menu_buttons: List[InlineKeyboardButton] = []
        button_1: InlineKeyboardButton = InlineKeyboardButton(text=sub_menu_data[i], callback_data=sub_menu_data[i])
        sub_menu_buttons.append(button_1)
        if i + 1 < len_symbol_list:
            button_2: InlineKeyboardButton = InlineKeyboardButton(text=sub_menu_data[i+1], callback_data=sub_menu_data[i+1])
            sub_menu_buttons.append(button_2)
        else:
            keyboard.add(*sub_menu_buttons)
            break
        if i + 2 < len_symbol_list:
            button_3: InlineKeyboardButton = InlineKeyboardButton(text=sub_menu_data[i+2], callback_data=sub_menu_data[i+2])
            sub_menu_buttons.append(button_3)
        else:
            keyboard.add(*sub_menu_buttons)
            break

        keyboard.add(*sub_menu_buttons)
    
    if call_data == SELECT_ALL.callback_data:
        select_button = UNSELECT_ALL
    else:
        select_button = SELECT_ALL

    if page == 0:
        keyboard.add(*[select_button, NEXT])
    elif page + 1 == final_page:
        keyboard.add(*[PREV, select_button])
    else:
        keyboard.add(*[PREV, select_button, NEXT])
    
    keyboard.add(*[MAIN_MENU])

    
    return (keyboard, f"Crypto symbols. Page {page + 1}/{final_page}")



if __name__ == "__main__":
    print(301 // 30 + 301 % 30)


