"""
tools/github_info.py
Look up GitHub user or repository info using the public GitHub API (no key needed).
"""

import requests

HEADERS = {"User-Agent": "AI-Agent-Tool", "Accept": "application/vnd.github+json"}


def execute(arguments: dict):
    query = arguments.get("query")

    if not query:
        return "GitHub info error: need a 'query' (username, or 'owner/repo' for a repository)"

    query = query.strip()

    try:
        if "/" in query:
            url = f"https://api.github.com/repos/{query}"
            response = requests.get(url, headers=HEADERS, timeout=8)
            if response.status_code == 404:
                return f"GitHub info error: repository '{query}' not found"
            response.raise_for_status()
            data = response.json()

            return (
                f"{data.get('full_name')}: {data.get('description') or 'No description'}\n"
                f"Stars: {data.get('stargazers_count')} | Forks: {data.get('forks_count')} | "
                f"Language: {data.get('language')}\n"
                f"URL: {data.get('html_url')}"
            )
        else:
            url = f"https://api.github.com/users/{query}"
            response = requests.get(url, headers=HEADERS, timeout=8)
            if response.status_code == 404:
                return f"GitHub info error: user '{query}' not found"
            response.raise_for_status()
            data = response.json()

            return (
                f"{data.get('name') or data.get('login')} (@{data.get('login')})\n"
                f"Bio: {data.get('bio') or 'No bio'}\n"
                f"Public repos: {data.get('public_repos')} | Followers: {data.get('followers')}\n"
                f"URL: {data.get('html_url')}"
            )

    except requests.exceptions.RequestException as e:
        return f"GitHub info error: could not reach GitHub ({e})"
    except Exception as e:
        return f"GitHub info error: {e}"


if __name__ == "__main__":
    print(execute({"query": "ayushxdev01"}))
    print(execute({"query": "torvalds/linux"}))