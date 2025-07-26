from datetime import datetime
from telebot.types import Message

from tg_bot.loader import bot
from tg_bot.states import BotStates

from tg_bot.services import analyze_market

from database.models import session, Settings, Users

@bot.message_handler(commands=["analyze_market"], state=BotStates.other_state)
def handle_analyze_market(message: Message) -> None:
    bot.set_state(message.from_user.id, state=BotStates.analyze_market)
    
    username: str = message.from_user.username

    user_settings_id: int = session.query(Users.settings_id).filter(Users.name == username).one()[0]
    user_settings = session.query(Settings).filter(Settings.id == user_settings_id).one()
    # print(user_settings.symbols)
    symbols = user_settings.symbols

    if len(symbols) == 0:
        bot.send_message(message.chat.id, "No symbols selected, please, choose symbols in \"Crypto symbols\" /settings")
    else:
        bot.send_message(message.chat.id, f"🕒 Analyzing market... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        while bot.get_state(message.from_user.id, message.chat.id) == "BotStates:analyze_market":
            for symbol in symbols:
                data = analyze_market(user_settings.oi_timeframe, 1, symbol)
                if data is None:
                    continue
                if bot.get_state(message.from_user.id, message.chat.id) != "BotStates:analyze_market":
                    break
                bot.send_message(message.chat.id, data, parse_mode="markdown")

            if bot.get_state(message.from_user.id, message.chat.id) != "BotStates:analyze_market":
                    break
                


@bot.message_handler(commands=["analyze_market", "settings", "start"], state=BotStates.analyze_market)
def handle_stop_analyze_market(message: Message) -> None:
    bot.set_state(message.from_user.id, state=BotStates.other_state)

