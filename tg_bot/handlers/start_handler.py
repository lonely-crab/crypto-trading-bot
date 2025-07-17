from telebot.types import Message
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from tg_bot.loader import bot
from database.models import session, Users, Settings


@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    username: str = message.from_user.username
    user = session.query(Users.name).filter(Users.name == username).one_or_none()
    if user:
        bot.send_message(chat_id=message.chat.id, text=f"Welcome back, {username}!")
    else:    
        try:
            settings = Settings()
            user = Users(name=username, settings=settings)
            session.add(user)
            bot.send_message(message.chat.id, f"Hello, {username}!")
            users = session.query(Users).all()
            bot.send_message(chat_id=message.chat.id, text=f"{[user.to_json() for user in users]}")
        except (IntegrityError, PendingRollbackError) as e:
            print(e)
        finally:
            session.commit()
            session.close()