from telebot.handler_backends import StatesGroup, State

class BotStates(StatesGroup):
    other_state = State()
    analyze_market = State()

