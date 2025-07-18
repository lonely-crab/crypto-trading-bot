from telebot.types import CallbackQuery
from typing import List, Tuple, Any, Optional, Union

from tg_bot.services.service import get_all_tickers
from tg_bot.config import SETTINGS_OPTIONS, OI_TIMEFRAMES, EXCHANGES, LANGUAGES


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