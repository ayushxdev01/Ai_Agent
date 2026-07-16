"""
tools/stock_price.py
Live stock price lookup using Yahoo Finance's public endpoint (no API key needed).
Understands company names (Apple, Tata Motors, Reliance) as well as raw tickers.
"""

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# Common company name -> ticker mapping (covers frequent everyday asks)
STOCK_ALIASES = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL", "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META", "facebook": "META",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "netflix": "NFLX",
    "intel": "INTC",
    "amd": "AMD",

    "reliance": "RELIANCE.NS", "reliance industries": "RELIANCE.NS",

    "tcs": "TCS.NS", "tata consultancy": "TCS.NS", "tata consultancy services": "TCS.NS",
    "infosys": "INFY.NS", "infy": "INFY.NS",
    "tata motors": "TMPV.NS", "tata motors passenger vehicles": "TMPV.NS", "tmpv": "TMPV.NS",
    "tata steel": "TATASTEEL.NS",
    "tata power": "TATAPOWER.NS",
    "tata chemicals": "TATACHEM.NS",
    "titan": "TITAN.NS", "titan company": "TITAN.NS",
    "tata consumer": "TATACONSUM.NS", "tata consumer products": "TATACONSUM.NS",
    "trent": "TRENT.NS",
    "tata elxsi": "TATAELXSI.NS",
    "voltas": "VOLTAS.NS",
    "tata communications": "TATACOMM.NS",

    "hdfc bank": "HDFCBANK.NS", "hdfc": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS", "icici": "ICICIBANK.NS",
    "sbi": "SBIN.NS", "state bank of india": "SBIN.NS",
    "wipro": "WIPRO.NS",
    "adani enterprises": "ADANIENT.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "airtel": "BHARTIARTL.NS", "bharti airtel": "BHARTIARTL.NS",
    "itc": "ITC.NS",
    "maruti": "MARUTI.NS", "maruti suzuki": "MARUTI.NS",
    "hindustan unilever": "HINDUNILVR.NS", "hul": "HINDUNILVR.NS",
    "l&t": "LT.NS", "larsen and toubro": "LT.NS", "larsen toubro": "LT.NS",
}

# Ambiguous group/umbrella names that map to MULTIPLE real companies.
# When the user just says the group name, give a friendly nudge instead of a raw "not found".
GROUP_HINTS = {
    "tata": ["Tata Motors", "TCS", "Tata Steel", "Tata Power", "Titan", "Tata Chemicals", "Tata Consumer"],
    "reliance group": ["Reliance", "Reliance Industries"],
    "adani": ["Adani Enterprises", "Adani Ports", "Adani Power", "Adani Green"],
    "birla": ["Aditya Birla Fashion", "Ultratech Cement", "Grasim"],
}


def resolve_symbol(value: str) -> str:
    if not value:
        return None
    cleaned = value.strip().lower()
    if cleaned in STOCK_ALIASES:
        return STOCK_ALIASES[cleaned]
    return value.strip().upper()


def _fetch(symbol: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    response = requests.get(url, headers=HEADERS, timeout=8)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    data = response.json()
    result = data.get("chart", {}).get("result")
    if not result:
        return None
    meta = result[0].get("meta", {})
    if meta.get("regularMarketPrice") is None:
        return None
    return meta


def execute(arguments: dict):
    raw_symbol = arguments.get("symbol")

    if not raw_symbol:
        return "Stock price error: need a 'symbol' or company name (e.g. AAPL, Apple, Reliance)"

    cleaned_input = raw_symbol.strip().lower()

    # Ambiguous group name (e.g. just "Tata") -> guide the user instead of failing silently
    if cleaned_input in GROUP_HINTS:
        options = ", ".join(GROUP_HINTS[cleaned_input])
        return (
            f"'{raw_symbol}' refers to a group of companies, not a single stock. "
            f"Did you mean one of these? {options}. "
            f"Please ask again with the specific company name."
        )

    symbol = resolve_symbol(raw_symbol)

    try:
        meta = _fetch(symbol)

        # If plain ticker fails and it doesn't already have an exchange suffix,
        # retry as an NSE-listed stock (common case for Indian companies typed in English)
        if meta is None and "." not in symbol:
            meta = _fetch(f"{symbol}.NS")
            if meta is not None:
                symbol = f"{symbol}.NS"

        if meta is None:
            return (
                f"Stock price error: could not find data for '{raw_symbol}'. "
                f"Try being more specific (e.g. 'Tata Motors' instead of 'Tata'), "
                f"or use the exact ticker (e.g. AAPL, RELIANCE.NS)."
            )

        price = meta.get("regularMarketPrice")
        currency = meta.get("currency", "")
        prev_close = meta.get("previousClose") or meta.get("chartPreviousClose")
        exchange_name = meta.get("fullExchangeName", "")

        change = ""
        if prev_close:
            diff = price - prev_close
            pct = (diff / prev_close) * 100
            direction = "up" if diff >= 0 else "down"
            change = f" ({direction} {abs(diff):.2f}, {abs(pct):.2f}% from previous close)"

        return f"{symbol} ({exchange_name}): {price} {currency}{change}"

    except requests.exceptions.RequestException as e:
        return f"Stock price error: could not reach data service ({e})"
    except Exception as e:
        return f"Stock price error: {e}"


if __name__ == "__main__":
    print(execute({"symbol": "Apple"}))
    print(execute({"symbol": "Reliance"}))
    print(execute({"symbol": "Tata Motors"}))
    print(execute({"symbol": "Tata Steel"}))
    print(execute({"symbol": "Titan"}))
    print(execute({"symbol": "Tata"}))