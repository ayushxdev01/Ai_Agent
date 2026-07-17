"""
tools/dictionary.py
English word definitions using the free dictionary API (no key needed).
"""

import requests


def execute(arguments: dict):
    word = arguments.get("word")

    if not word:
        return "Dictionary error: need a 'word' to look up"

    word = word.strip().lower()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 404:
            return f"Dictionary error: no definition found for '{word}'"
        response.raise_for_status()
        data = response.json()

        entry = data[0]
        meanings = entry.get("meanings", [])
        if not meanings:
            return f"Dictionary error: no definitions found for '{word}'"

        result_lines = [f"{word.capitalize()}:"]
        for meaning in meanings[:3]:
            part_of_speech = meaning.get("partOfSpeech", "")
            definitions = meaning.get("definitions", [])
            if definitions:
                definition_text = definitions[0].get("definition", "")
                result_lines.append(f"({part_of_speech}) {definition_text}")

        return "\n".join(result_lines)

    except requests.exceptions.RequestException as e:
        return f"Dictionary error: could not reach data service ({e})"
    except Exception as e:
        return f"Dictionary error: {e}"


if __name__ == "__main__":
    print(execute({"word": "ephemeral"}))