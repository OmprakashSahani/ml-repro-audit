from urllib.parse import urlparse

import requests


GITHUB_API_BASE = "https://api.github.com"


def parse_github_url(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)

    if parsed.netloc != "github.com":
        raise ValueError("Only GitHub URLs are supported")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    return parts[0], parts[1]


def fetch_repo_metadata(owner: str, repo: str) -> dict:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"

    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        raise ValueError("Repository not found")

    if response.status_code != 200:
        raise ValueError(f"GitHub API error: {response.status_code}")

    return response.json()