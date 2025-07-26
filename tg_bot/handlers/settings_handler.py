from telebot.types import Message, CallbackQuery
from typing import List, Tuple, Any, Optional, Union
from telebot.types import InlineKeyboardMarkup  # move


from tg_bot.loader import bot
from tg_bot.config import SETTINGS_OPTIONS, OI_TIMEFRAMES, EXCHANGES, LANGUAGES
from tg_bot.states import BotStates

from tg_bot.keyboards.inline import create_settings_keyboard_subgeneral, create_settings_keyboard_general, create_symbols_keyboard, NEXT, PREV, SELECT_ALL, UNSELECT_ALL
from tg_bot.utils import update_chosen_timeframe, update_chosen_symbols
from tg_bot.services import get_all_tickers


@bot.message_handler(commands=["settings"], state=BotStates.other_state)
def handle_settings(message: Message) -> None:
    keyboard = create_settings_keyboard_general(SETTINGS_OPTIONS)
    bot.send_message(chat_id=message.chat.id, text="Main Menu", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in [i[0] for i in SETTINGS_OPTIONS], state=BotStates.other_state)
def handle_sub_settings(call: CallbackQuery) -> None:
    if call.data == "Crypto Symbols":
        keyboard_tuple: Tuple[InlineKeyboardMarkup, Optional[str]] = create_symbols_keyboard(SETTINGS_OPTIONS, call)
    else:
        keyboard_tuple: Tuple[InlineKeyboardMarkup, Optional[str]] = create_settings_keyboard_subgeneral(SETTINGS_OPTIONS, call)
    keyboard = keyboard_tuple[0]
    keyboard_text: str = keyboard_tuple[1] if keyboard_tuple[1] else call.data # type: ignore
    bot.edit_message_text(text=keyboard_text, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in [NEXT.callback_data, PREV.callback_data], state=BotStates.other_state)
def handle_next_prev(call: CallbackQuery) -> None:
    keyboard_tuple: Tuple[InlineKeyboardMarkup, Optional[str]] = create_symbols_keyboard(SETTINGS_OPTIONS, call)
    keyboard = keyboard_tuple[0]
    keyboard_text: str = keyboard_tuple[1] if keyboard_tuple[1] else call.data # type: ignore
    print(keyboard_text)
    bot.edit_message_text(text=keyboard_text, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "main_menu", state=BotStates.other_state)
def handle_return_to_main_settings(call: CallbackQuery) -> None:
    keyboard = create_settings_keyboard_general(SETTINGS_OPTIONS)
    bot.edit_message_text(chat_id=call.message.chat.id, text="Main Menu", message_id=call.message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in OI_TIMEFRAMES, state=BotStates.other_state)
def handle_oi_timeframe_settings(call: CallbackQuery) -> None:
    update_chosen_timeframe(call)
    keyboard_tuple: Tuple[InlineKeyboardMarkup, Optional[str]] = create_settings_keyboard_subgeneral(SETTINGS_OPTIONS, call)
    keyboard = keyboard_tuple[0]
    keyboard_text: str = "Timeframe" # type: ignore
    bot.edit_message_text(text=keyboard_text, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in get_all_tickers() or call.data.startswith("✅"), state=BotStates.other_state) # fix symbols retrieval
def handle_crypto_symbols_settings(call: CallbackQuery) -> None:
    all_symbols: List[str] = get_all_tickers()
    update_chosen_symbols(call, all_symbols)
    keyboard_tuple: Tuple[InlineKeyboardMarkup, Optional[str]] = create_symbols_keyboard(SETTINGS_OPTIONS, call)
    keyboard = keyboard_tuple[0]
    keyboard_text: str = keyboard_tuple[1] if keyboard_tuple[1] else call.data # type: ignore
    bot.edit_message_text(text=keyboard_text, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in [SELECT_ALL.callback_data, UNSELECT_ALL.callback_data], state=BotStates.other_state)
def handle_selection_unselection(call: CallbackQuery) -> None:
    all_symbols: List[str] = get_all_tickers()
    update_chosen_symbols(call, all_symbols)
    keyboard_tuple: Tuple[InlineKeyboardMarkup, Optional[str]] = create_symbols_keyboard(SETTINGS_OPTIONS, call)
    keyboard = keyboard_tuple[0]
    keyboard_text: str = keyboard_tuple[1] if keyboard_tuple[1] else call.data # type: ignore
    bot.edit_message_text(text=keyboard_text, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)


