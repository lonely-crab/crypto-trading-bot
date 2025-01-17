from telebot.types import Message

from tg_bot.loader import bot

@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.username}")