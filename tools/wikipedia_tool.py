"""
tools/wikipedia_tool.py
Quick factual lookups from Wikipedia.
Requires: pip install wikipedia
"""


def execute(arguments: dict):
    query = arguments.get("query")

    if not query:
        return "Wikipedia error: no 'query' provided"

    try:
        import wikipedia
    except ImportError:
        return "Wikipedia error: package not installed. Run: pip install wikipedia"

    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True)
        return summary

    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:5])
        return f"'{query}' is ambiguous. Did you mean: {options}?"

    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'."

    except Exception as e:
        return f"Wikipedia error: {e}"


if __name__ == "__main__":
    print(execute({"query": "Alan Turing"}))    