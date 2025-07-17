from tg_bot.config import TELEGRAM_TOKEN
import tg_bot.handlers  # noqa
from tg_bot.loader import bot
from tg_bot.utils import set_default_commands

from database.models import Base, engine


if __name__ == "__main__":
    set_default_commands(bot)
    print("Bot is running...")
    Base.metadata.create_all(engine)
    bot.infinity_polling()