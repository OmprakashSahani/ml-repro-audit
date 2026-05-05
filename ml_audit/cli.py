import argparse

from ml_audit.analyzer.repo_structure import analyze_repo_files
from ml_audit.github_api import (
    fetch_repo_files,
    fetch_repo_metadata,
    parse_github_url,
)
from ml_audit.scoring import compute_reproducibility_score


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
        files = fetch_repo_files(owner, repo)
        analysis = analyze_repo_files(files)
        score, breakdown = compute_reproducibility_score(analysis)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print(f"Repository: {metadata['full_name']}")
    print(f"Stars: {metadata['stargazers_count']}")
    print()

    print("Structure Analysis:")
    for key, value in analysis.items():
        print(f"- {key}: {'YES' if value else 'NO'}")

    print()
    print(f"Reproducibility Score: {score:.1f}/10")
    print("Breakdown:")
    for key, value in breakdown.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()