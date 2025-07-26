from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from tg_bot.config import TELEGRAM_TOKEN

storage = StateMemoryStorage()

bot = TeleBot(TELEGRAM_TOKEN, state_storage=storage)