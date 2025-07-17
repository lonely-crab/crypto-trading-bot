from pybit.unified_trading import HTTP
import time
from datetime import datetime, timedelta

from ..config import BYBIT_API_KEY, BYBIT_API_SECRET

from typing import Dict, List, Optional, Any, Union


# ==== Конфигурация пользователя ====


TIMEFRAME_MINUTES = 5            # Таймфрейм анализа в минутах: 1, 5, 15, 30 и т.д.
MIN_PERCENT_CHANGE = 3            # Минимальный процент изменения OI или цены
SLEEP_BETWEEN_CHECKS = 1 * 60  # В секундах
SIGNALS_COUNT = {}                # Счётчик сигналов за 24 часа

# ==== Подключение к ByBit ====
session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

def get_all_tickers() -> Optional[List[str]]:
    """Получает список всех доступных USDT-пар."""
    response: Union[Dict, Any] = session.get_tickers(category="linear")
    print("Currencies retrieved. Receiving oi and price.")
    return [ticker["symbol"] for ticker in response["result"]["list"] if ticker["symbol"].endswith("USDT")]


def get_oi_and_price(symbol, interval_minutes: int):
    """
    Получает данные об изменении OI и цены за интервал времени.
    Возвращает:
        - процент изменения OI
        - абсолютное изменение OI (в миллионах $)
        - процент изменения цены
        - последнюю цену
    """
    now = int(time.time()) * 1000
    # start = now - (interval_minutes * 60 * 1000)

    try:
        # Получение OI
        oi_response = session.get_open_interest(
            category="linear",
            symbol=symbol,
            intervalTime=''.join([str(interval_minutes), "min"]),
            # startTime=start,
            endTime=now,
            limit=2
        )

        # Получение цены (закрытия свечи)
        price_response = session.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval_minutes,
            # start=start,
            end=now,
            limit=2
        )

        oi_data = oi_response["result"]["list"]
        price_data = price_response["result"]["list"]

        # # test purposes
        # print(oi_data)
        # print(price_data)


        if len(oi_data) < 2 or len(price_data) < 2:
            return None, None, None, None, None, None

        oi_start = float(oi_data[1]["openInterest"])
        oi_end = float(oi_data[0]["openInterest"])
        oi_change = ((oi_end - oi_start) / oi_start) * 100
        oi_change_abs = (oi_end - oi_start) / 1_000_000  # в миллионах долларов

        price_start = float(price_data[1][4])  # close
        price_end = float(price_data[0][4])
        price_change = ((price_end - price_start) / price_start) * 100

        print(f"[SUCCESS] Retrieved oi and price for {symbol}")
        return oi_change, oi_change_abs, price_change, price_end, oi_data[0]["timestamp"], oi_data[1]["timestamp"]

    except Exception as e:
        print(f"[ERROR] Failed for {symbol}: {e}")
        return None, None, None, None, None, None
    

# if __name__ == "__main__":
#     symbols = get_all_tickers()
#     for symbol in symbols:
#         print(get_oi_and_price(symbol, TIMEFRAME_MINUTES))


def analyze_market(interval_minutes: int, min_percent: float):
    """Основная функция анализа рынка по всем монетам."""
    tickers = get_all_tickers()
    print(f"\n🕒 Analyzing market... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for symbol in tickers:
        oi_change, oi_change_abs, price_change, price_end, end, start = get_oi_and_price(symbol, interval_minutes)
        
        start = datetime.fromtimestamp(int(start) / 1000)
        end = datetime.fromtimestamp(int(end) / 1000)
        if oi_change is None or price_change is None:
            continue

        if abs(oi_change) >= min_percent or abs(price_change) >= min_percent:
            # Считаем количество сигналов за 24 часа
            SIGNALS_COUNT[symbol] = SIGNALS_COUNT.get(symbol, 0) + 1

            
            print(f"Interval: {start} - {end}")
            print(f"\n📺 ByBit — ⌚️{interval_minutes}m — {symbol}")
            direction = "increased" if oi_change > 0 else "decreased"
            print(f"📉 OI {direction} by {oi_change:.2f}% ({oi_change_abs:.2f}M $)")
            print(f"💱 Price change: {price_change:.2f}%")
            print(f"\n🔁 Count of signals per 24h: {SIGNALS_COUNT[symbol]}")

if __name__ == "__main__":
    while True:
        analyze_market(
            interval_minutes=TIMEFRAME_MINUTES,
            min_percent=MIN_PERCENT_CHANGE
        )
        print(f"\n⏳ Sleeping for {TIMEFRAME_MINUTES} minutes...\n")
        time.sleep(SLEEP_BETWEEN_CHECKS)
