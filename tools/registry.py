from tools.calculator import execute as calculator
from tools.time_tool import execute as time_tool
from tools.weather import execute as weather
from tools.currency_converter import execute as currency_converter
from tools.wikipedia_tool import execute as wikipedia_lookup
from tools.unit_converter import execute as unit_converter
from tools.web_search import execute as web_search
from tools.stock_price import execute as stock_price
from tools.qr_code import execute as qr_code
from tools.crypto_price import execute as crypto_price
from tools.github_info import execute as github_info
from tools.dictionary import execute as dictionary

TOOLS = {
    "calculator": calculator,
    "time": time_tool,
    "weather": weather,
    "currency_converter": currency_converter,
    "wikipedia": wikipedia_lookup,
    "unit_converter": unit_converter,
    "web_search": web_search,
    "stock_price": stock_price,
    "qr_code": qr_code,
    "crypto_price": crypto_price,
    "github_info": github_info,
    "dictionary": dictionary,
}


def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Unknown Tool: {tool_name}"

    return tool(arguments)


def list_tools():
    return list(TOOLS.keys())