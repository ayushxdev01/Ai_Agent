"""
tools/web_search.py
Live web search using DuckDuckGo (no API key required).
Requires: pip install ddgs
"""


def execute(arguments: dict):
    query = arguments.get("query")

    if not query:
        return "Web search error: no 'query' provided"

    try:
        from ddgs import DDGS
    except ImportError:
        return "Web search error: package not installed. Run: pip install ddgs"

    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                title = r.get("title", "").strip()
                body = r.get("body", "").strip()
                href = r.get("href", "").strip()
                results.append(f"- {title}: {body} ({href})")

        if not results:
            return f"No web results found for '{query}'."

        return "Web search results:\n" + "\n".join(results)

    except Exception as e:
        return f"Web search error: {e}"


if __name__ == "__main__":
    print(execute({"query": "latest AI news India"}))