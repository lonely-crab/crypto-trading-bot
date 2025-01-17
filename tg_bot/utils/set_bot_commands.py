from telebot.types import BotCommand
from telebot import TeleBot

from tg_bot.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])