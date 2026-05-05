import argparse

from ml_audit.github_api import fetch_repo_metadata, parse_github_url


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ml-audit",
        description="Audit ML repositories for reproducibility and systems quality.",
    )

    parser.add_argument(
        "repo_url",
        nargs="?",
        help="GitHub repository URL to audit",
    )

    args = parser.parse_args()

    if not args.repo_url:
        parser.print_help()
        return

    try:
        owner, repo = parse_github_url(args.repo_url)
        metadata = fetch_repo_metadata(owner, repo)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print(f"Repository: {metadata['full_name']}")
    print(f"Description: {metadata.get('description')}")
    print(f"Stars: {metadata['stargazers_count']}")
    print(f"Forks: {metadata['forks_count']}")
    print(f"Language: {metadata.get('language')}")