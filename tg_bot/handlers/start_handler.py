from telebot.types import Message
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from tg_bot.loader import bot
from tg_bot.states import BotStates

from database.models import session, Users, Settings


@bot.message_handler(commands=["start"], state=None)
def handle_start(message: Message):
    """
    Handles the /start command from Telegram users.

    This function checks if the user already exists in the database.
    - If the user exists, it sends a welcome-back message.
    - If the user is new, it:
        1. Creates a new Settings object with default values.
        2. Creates a new User with the associated settings.
        3. Adds the user to the database.
        4. Sends a greeting message.

    Exceptions:
        - Catches IntegrityError and PendingRollbackError to avoid breaking on DB inconsistencies.
    
    Notes:
        - Always commits or rolls back the session and ensures it's closed properly.
    """
    bot.set_state(message.from_user.id, BotStates.other_state)
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
        except (IntegrityError, PendingRollbackError) as e:
            print(e)
        finally:
            session.commit()
            session.close()
