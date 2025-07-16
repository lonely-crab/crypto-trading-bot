from tg_bot.config import TELEGRAM_TOKEN
import tg_bot.handlers
from tg_bot.loader import bot
from tg_bot.utils import set_default_commands


if __name__ == "__main__":
    set_default_commands(bot)
    print("Bot is running...")
    bot.infinity_polling(restart_on_change=True)