import base64
import os
from urllib.parse import urlparse

import requests


GITHUB_API_BASE = "https://api.github.com"


def get_headers() -> dict:
    token = os.getenv("GITHUB_TOKEN")

    if token:
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

    return {}


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

    response = requests.get(url, headers=get_headers(), timeout=10)

    if response.status_code == 404:
        raise ValueError("Repository not found")

    if response.status_code == 403:
        raise ValueError(
            "GitHub API rate limit reached. Set GITHUB_TOKEN to increase the limit."
        )

    if response.status_code != 200:
        raise ValueError(f"GitHub API error: {response.status_code}")

    return response.json()


def fetch_repo_files(owner: str, repo: str) -> list[str]:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"

    response = requests.get(url, headers=get_headers(), timeout=10)

    if response.status_code == 403:
        raise ValueError(
            "GitHub API rate limit reached. Set GITHUB_TOKEN to increase the limit."
        )

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch repo files: {response.status_code}")

    data = response.json()

    return [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]


def fetch_file_content(owner: str, repo: str, path: str) -> str:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"

    response = requests.get(url, headers=get_headers(), timeout=10)

    if response.status_code != 200:
        return ""

    data = response.json()

    if data.get("encoding") == "base64":
        try:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        except Exception:
            return ""

    return ""