from dotenv import load_dotenv
import os


load_dotenv()

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")


# default bot commands
DEFAULT_COMMANDS = [
    ("start", "Start bot"),
    ("analyze_market", "Analyze market"),
    ("settings", "Settings")

]

# settings options in main menu for command /settings
SETTINGS_OPTIONS = [
    ("Timeframe", "in development"),
    ("Crypto Symbols", "in development"),
    ("Exchange", "in development"),
    ("Language", "in development"),
]

# available timeframes for open interest
OI_TIMEFRAMES = [
    "5min",
    "15min",
    "30min",
    "1h",
    "4h",
    "1d"
]

# available exchanges 
EXCHANGES = [
    ("ByBit", "https://www.bybit.com/en/"),
]

# available languages
LANGUAGES = [
    "English",
    "Russian"
]


# temporary user settings
USER_SETTINGS = {
    "language": "English",
    "exchange": "Bybit",
    "timeframe": "5min",
    "symbols": "all",
}