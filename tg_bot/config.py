from dotenv import load_dotenv
import os


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")


DEFAULT_COMMANDS = [
    ("start", "Start bot"),

]
