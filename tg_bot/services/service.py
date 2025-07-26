from pybit.unified_trading import HTTP
import time
from datetime import datetime, timedelta

from tg_bot.config import BYBIT_API_KEY, BYBIT_API_SECRET


from typing import Dict, List, Optional, Any, Union

SIGNALS_COUNT = {}

# ==== Подключение к ByBit ====
http_session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

def get_all_tickers() -> Optional[List[str]]:
    """Получает список всех доступных USDT-пар."""
    response: Union[Dict, Any] = http_session.get_tickers(category="linear")
    print("Currencies retrieved. Receiving oi and price.")
    return [ticker["symbol"] for ticker in response["result"]["list"] if ticker["symbol"].endswith("USDT")]


def get_oi_and_price(symbol, interval_minutes: str):
    """
    Получает данные об изменении OI и цены за интервал времени.
    Возвращает:
        - процент изменения OI
        - абсолютное изменение OI (в миллионах $)
        - процент изменения цены
        - последнюю цену
    """
    now = int(time.time()) * 1000

    try:
        # Получение OI
        oi_response = http_session.get_open_interest(
            category="linear",
            symbol=symbol,
            intervalTime=interval_minutes,
            endTime=now,
            limit=2
        )

        # Получение цены (закрытия свечи)
        price_response = http_session.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval_minutes.strip("min"),
            end=now,
            limit=2
        )

        oi_data = oi_response["result"]["list"]
        price_data = price_response["result"]["list"]


        if len(oi_data) < 2 or len(price_data) < 2:
            return None, None, None, None, None, None

        oi_start = float(oi_data[1]["openInterest"])
        oi_end = float(oi_data[0]["openInterest"])
        oi_change = ((oi_end - oi_start) / oi_start) * 100
        oi_change_abs = (oi_end - oi_start) / 1_000_000  

        price_start = float(price_data[1][4])  
        price_end = float(price_data[0][4])
        price_change = ((price_end - price_start) / price_start) * 100

        return oi_change, oi_change_abs, price_change, price_end, oi_data[0]["timestamp"], oi_data[1]["timestamp"]

    except Exception as e:
        print(f"[ERROR] Failed for {symbol}: {e}")
        return None, None, None, None, None, None



def analyze_market(interval_minutes: str, min_percent: float, symbol: str) -> Optional[str]:
    """Основная функция анализа рынка по всем монетам.
    
    Returns:
        str: Отформатированный текст с результатами анализа.
    """

    # print(f"\n🕒 Analyzing market... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Собираем вывод в строку
    result_lines = []

    oi_change, oi_change_abs, price_change, price_end, end, start = get_oi_and_price(symbol, interval_minutes)
    try:
        start_dt = datetime.fromtimestamp(int(start) / 1000)
        end_dt = datetime.fromtimestamp(int(end) / 1000)
    except Exception as e:
        result_lines.append(f"[ERROR] {symbol}: {e}")
        return None

    if oi_change is None or price_change is None:
        return None

    if abs(oi_change) >= min_percent or abs(price_change) >= min_percent:
        # Считаем количество сигналов за 24 часа
        SIGNALS_COUNT[symbol] = SIGNALS_COUNT.get(symbol, 0) + 1

        result_lines.append(f"Interval: {start_dt} - {end_dt}")
        result_lines.append(f"\n📺 [ByBit](https://www.bybit.com/trade/usdt/{symbol}) — ⌚️{interval_minutes} — [{symbol}](https://www.coinglass.com/tv/Bybit_{symbol})")
        direction = "increased" if oi_change > 0 else "decreased"
        result_lines.append(f"📉 OI {direction} by {oi_change:.2f}% ({oi_change_abs:.2f}M $)")
        result_lines.append(f"💱 Price change: {price_change:.2f}%")
        result_lines.append(f"\n🔁 Count of signals per 24h: {SIGNALS_COUNT[symbol]}")
        result_lines.append("")  # пустая строка для разделения

    # Если ни одного сигнала не найдено
    if not result_lines:
        return None

    # Объединяем всё в одну строку
    return "\n".join(result_lines)

