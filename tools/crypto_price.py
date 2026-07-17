"""
tools/crypto_price.py
Live cryptocurrency price using CoinGecko's free public API (no key needed).
"""

import requests

CRYPTO_ALIASES = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "solana": "solana", "sol": "solana",
    "ripple": "ripple", "xrp": "ripple",
    "cardano": "cardano", "ada": "cardano",
    "litecoin": "litecoin", "ltc": "litecoin",
    "polkadot": "polkadot", "dot": "polkadot",
    "shiba inu": "shiba-inu", "shib": "shiba-inu",
    "binance coin": "binancecoin", "bnb": "binancecoin",
}


def execute(arguments: dict):
    coin = arguments.get("coin")
    currency = arguments.get("currency", "usd").lower()

    if not coin:
        return "Crypto price error: need a 'coin' name (e.g. Bitcoin, Ethereum)"

    coin_id = CRYPTO_ALIASES.get(coin.strip().lower(), coin.strip().lower())

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id, "vs_currencies": currency, "include_24hr_change": "true"}

    try:
        response = requests.get(url, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()

        if coin_id not in data:
            return f"Crypto price error: could not find '{coin}'. Try the common name (e.g. Bitcoin, Ethereum, Dogecoin)."

        price = data[coin_id].get(currency)
        change = data[coin_id].get(f"{currency}_24h_change")

        change_text = f" ({'up' if change >= 0 else 'down'} {abs(change):.2f}% in 24h)" if change is not None else ""

        return f"{coin.title()}: {price} {currency.upper()}{change_text}"

    except requests.exceptions.RequestException as e:
        return f"Crypto price error: could not reach data service ({e})"
    except Exception as e:
        return f"Crypto price error: {e}"


if __name__ == "__main__":
    print(execute({"coin": "Bitcoin"}))
    print(execute({"coin": "Ethereum"}))