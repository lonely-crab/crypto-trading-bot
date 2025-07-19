from telebot.types import CallbackQuery
from typing import List, Tuple, Any, Optional, Union

from tg_bot.services.service import get_all_tickers
from tg_bot.config import SETTINGS_OPTIONS, OI_TIMEFRAMES, EXCHANGES, LANGUAGES
from tg_bot.keyboards.inline import NEXT, PREV

from database.models import session, Users, Settings


# (move) function for handling choice of data for sub menu
def retrieve_data_for_sub_menu(settings_list: List[Tuple[str, str]], call: CallbackQuery) -> Optional[List[str] | str]:
    sub_menus: List[str] = [setting[0] for setting in settings_list]
    call_data: Optional[str] = call.data

    # check if setting exists
    if call_data not in sub_menus and call_data not in [NEXT.callback_data, PREV.callback_data]:
        return
    try:
        # check if setting is not in development
        if settings_list[sub_menus.index(call_data)][1] == "in development":
            return "Sorry, this segment is in development"
    except ValueError:
        pass
    
    username: str = call.from_user.username

    # choose data for retrieval
    if call_data == "Timeframe":
        return get_chosen_settings(OI_TIMEFRAMES.copy(), "oi_timeframe", username)
    elif call_data == "Exchange":
        return get_chosen_settings(EXCHANGES.copy(), "exchanges", username)
    elif call_data == "Language":
        return get_chosen_settings(LANGUAGES.copy(), "language", username)
    elif call_data == "Crypto Symbols" or call_data in [NEXT.callback_data, PREV.callback_data]:
        return get_chosen_settings([], "symbols", username)
    

def get_chosen_settings(sub_settings: List[str], setting_name: str, username: str) -> List[str]:
    user_settings_id: int = session.query(Users.settings_id).filter(Users.name == username).one()[0]
    
    if setting_name == "oi_timeframe":
        selected_option: str = session.query(Settings.oi_timeframe).filter(Settings.id == user_settings_id).one()[0]
        sub_settings[sub_settings.index(selected_option)] = ' '.join(["✅", selected_option])
    elif setting_name == "exchanges":
        selected_option: str = session.query(Settings.exchanges).filter(Settings.id == user_settings_id).one()[0]
        for option in selected_option:
            if option in sub_settings:
                sub_settings[sub_settings.index(option)] = ' '.join(["✅", option])
    elif setting_name == "language":
        selected_option: str = session.query(Settings.language).filter(Settings.id == user_settings_id).one()[0]
        sub_settings[sub_settings.index(selected_option)] = ' '.join(["✅", selected_option])
    elif setting_name == "symbols":
        symbols_available: Optional[List[str]] = get_all_tickers()
        sub_settings: List[str] = get_chosen_symbols(setting_name, username, symbols_available, user_settings_id)
    

    return sub_settings


def get_chosen_symbols(setting_name: str, username: str, symbols_available: List[str], user_settings_id: int) -> List[str]:
    amount_symbols_available: int = len(symbols_available)
    sym_list: List[str] = symbols_available.copy()


    selected_symbols: List[str] = session.query(Settings.symbols).filter(Settings.id == user_settings_id).one()[0]

    if len(selected_symbols) >= amount_symbols_available:
        for symbol in sym_list:
            sym_list[sym_list.index(symbol)] = ' '.join(["✅", symbol])
    
    else:
        for symbol in selected_symbols:
            if symbol in sym_list:
                sym_list[sym_list.index(symbol)] =  ' '.join(["✅", symbol])
        
    return sym_list


if __name__ == "__main__":
    print(get_chosen_settings(OI_TIMEFRAMES, "oi_timeframe", "lonely_crab"))