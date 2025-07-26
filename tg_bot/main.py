from tg_bot.config import TELEGRAM_TOKEN
import tg_bot.handlers  # noqa
from tg_bot.loader import bot
from tg_bot.utils import set_default_commands

from database.models import Base, engine

from telebot.custom_filters import StateFilter

if __name__ == "__main__":
    set_default_commands(bot)
    print("Bot is running...")
    Base.metadata.create_all(engine)
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()