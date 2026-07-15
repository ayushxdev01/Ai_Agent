"""
tools/unit_converter.py
Converts values between length, weight, volume and temperature units.
No external API required.
"""

LENGTH = {
    "m": 1, "meter": 1, "meters": 1,
    "km": 1000, "kilometer": 1000, "kilometers": 1000,
    "cm": 0.01, "centimeter": 0.01, "centimeters": 0.01,
    "mm": 0.001, "millimeter": 0.001, "millimeters": 0.001,
    "mile": 1609.344, "miles": 1609.344, "mi": 1609.344,
    "yard": 0.9144, "yards": 0.9144, "yd": 0.9144,
    "foot": 0.3048, "feet": 0.3048, "ft": 0.3048,
    "inch": 0.0254, "inches": 0.0254, "in": 0.0254,
}

WEIGHT = {
    "g": 1, "gram": 1, "grams": 1,
    "kg": 1000, "kilogram": 1000, "kilograms": 1000,
    "mg": 0.001, "milligram": 0.001, "milligrams": 0.001,
    "lb": 453.592, "lbs": 453.592, "pound": 453.592, "pounds": 453.592,
    "oz": 28.3495, "ounce": 28.3495, "ounces": 28.3495,
}

VOLUME = {
    "l": 1, "liter": 1, "liters": 1, "litre": 1, "litres": 1,
    "ml": 0.001, "milliliter": 0.001, "milliliters": 0.001,
    "gallon": 3.78541, "gallons": 3.78541, "gal": 3.78541,
    "cup": 0.236588, "cups": 0.236588,
    "tbsp": 0.0147868, "tsp": 0.00492892,
}

TEMP_UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}


def _convert_temperature(value, from_unit, to_unit):
    fu, tu = from_unit.lower(), to_unit.lower()

    if fu in ("c", "celsius"):
        celsius = value
    elif fu in ("f", "fahrenheit"):
        celsius = (value - 32) * 5 / 9
    elif fu in ("k", "kelvin"):
        celsius = value - 273.15
    else:
        raise ValueError(f"Unknown temperature unit '{from_unit}'")

    if tu in ("c", "celsius"):
        return celsius
    elif tu in ("f", "fahrenheit"):
        return celsius * 9 / 5 + 32
    elif tu in ("k", "kelvin"):
        return celsius + 273.15
    else:
        raise ValueError(f"Unknown temperature unit '{to_unit}'")


def execute(arguments: dict):
    try:
        value = arguments.get("value")
        from_unit = arguments.get("from_unit")
        to_unit = arguments.get("to_unit")

        if value is None or not from_unit or not to_unit:
            return "Unit conversion error: need 'value', 'from_unit' and 'to_unit'"

        value = float(value)
        fu = str(from_unit).strip().lower()
        tu = str(to_unit).strip().lower()

        if fu in TEMP_UNITS and tu in TEMP_UNITS:
            result = _convert_temperature(value, fu, tu)
            return f"{value} {from_unit} = {round(result, 4)} {to_unit}"

        for table in (LENGTH, WEIGHT, VOLUME):
            if fu in table and tu in table:
                base = value * table[fu]
                result = base / table[tu]
                return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

        return f"Unit conversion error: unsupported or mismatched units '{from_unit}' -> '{to_unit}'"

    except Exception as e:
        return f"Unit conversion error: {e}"


if __name__ == "__main__":
    print(execute({"value": 10, "from_unit": "km", "to_unit": "miles"}))
    print(execute({"value": 100, "from_unit": "f", "to_unit": "c"}))