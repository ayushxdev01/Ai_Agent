"""
tools/currency_converter.py
Currency conversion using open.er-api.com (free, no API key needed).
Supports 160+ currencies including INR, AED, etc.
Handles both ISO codes (USD, INR) and common currency names (dollar, rupee, euro, yen).
"""

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

CURRENCY_ALIASES = {
    "dollar": "USD", "dollars": "USD", "usd": "USD", "us dollar": "USD", "$": "USD",
    "rupee": "INR", "rupees": "INR", "inr": "INR", "indian rupee": "INR", "₹": "INR",
    "euro": "EUR", "euros": "EUR", "eur": "EUR", "€": "EUR",
    "pound": "GBP", "pounds": "GBP", "gbp": "GBP", "british pound": "GBP", "£": "GBP",
    "yen": "JPY", "jpy": "JPY", "japanese yen": "JPY", "¥": "JPY",
    "yuan": "CNY", "cny": "CNY", "chinese yuan": "CNY", "rmb": "CNY",
    "franc": "CHF", "swiss franc": "CHF", "chf": "CHF",
    "dirham": "AED", "aed": "AED", "uae dirham": "AED",
    "riyal": "SAR", "sar": "SAR", "saudi riyal": "SAR",
    "singapore dollar": "SGD", "sgd": "SGD",
    "canadian dollar": "CAD", "cad": "CAD",
    "australian dollar": "AUD", "aud": "AUD",
    "won": "KRW", "krw": "KRW", "korean won": "KRW",
    "ringgit": "MYR", "myr": "MYR",
    "baht": "THB", "thb": "THB",
    "peso": "MXN", "mxn": "MXN", "mexican peso": "MXN",
    "real": "BRL", "brl": "BRL", "brazilian real": "BRL",
    "rand": "ZAR", "zar": "ZAR", "south african rand": "ZAR",
    "naira": "NGN", "ngn": "NGN",
    "ruble": "RUB", "rub": "RUB", "russian ruble": "RUB",
    "lira": "TRY", "try": "TRY", "turkish lira": "TRY",
}


def resolve_currency(value: str):
    if not value:
        return None
    cleaned = value.strip().lower()
    if cleaned in CURRENCY_ALIASES:
        return CURRENCY_ALIASES[cleaned]
    if len(cleaned) == 3 and cleaned.isalpha():
        return cleaned.upper()
    return value.strip().upper()


def execute(arguments: dict):
    amount = arguments.get("amount")
    from_currency = arguments.get("from_currency")
    to_currency = arguments.get("to_currency")

    if amount is None or not from_currency or not to_currency:
        return "Currency converter error: need 'amount', 'from_currency', and 'to_currency'"

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return f"Currency converter error: invalid amount '{amount}'"

    from_code = resolve_currency(from_currency)
    to_code = resolve_currency(to_currency)

    if not from_code or not to_code:
        return f"Currency converter error: could not understand currency '{from_currency}' or '{to_currency}'"

    url = f"https://open.er-api.com/v6/latest/{from_code}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            return f"Currency converter error: unsupported currency code '{from_code}'"

        rates = data.get("rates", {})
        rate = rates.get(to_code)

        if rate is None:
            return f"Currency converter error: unsupported currency code '{to_code}'"

        converted = round(amount * rate, 4)
        return f"{amount:g} {from_code} = {converted} {to_code}"

    except requests.exceptions.HTTPError as e:
        return f"Currency converter error: exchange rate service rejected the request ({e})"
    except requests.exceptions.RequestException as e:
        return f"Currency converter error: could not reach exchange rate service ({e})"
    except Exception as e:
        return f"Currency converter error: {e}"


if __name__ == "__main__":
    print(execute({"amount": 500, "from_currency": "euro", "to_currency": "yen"}))
    print(execute({"amount": 250, "from_currency": "rupees", "to_currency": "dirham"}))
    print(execute({"amount": 1000, "from_currency": "pounds", "to_currency": "singapore dollar"}))