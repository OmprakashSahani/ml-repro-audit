import argparse

from rich.console import Console
from rich.table import Table

from ml_audit.analyzer.repo_structure import analyze_repo_files
from ml_audit.github_api import (
    fetch_repo_files,
    fetch_repo_metadata,
    parse_github_url,
)
from ml_audit.scoring import compute_reproducibility_score


console = Console()


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
        console.print(f"[red]Error:[/red] {e}")
        return

    console.print(f"\n[bold cyan]Repository:[/bold cyan] {metadata['full_name']}")
    console.print(f"[bold]Stars:[/bold] {metadata['stargazers_count']}\n")

    # Structure Table
    table = Table(title="Structure Analysis")
    table.add_column("Check", style="bold")
    table.add_column("Status")

    for key, value in analysis.items():
        status = "[green]YES[/green]" if value else "[red]NO[/red]"
        table.add_row(key, status)

    console.print(table)

    # Score
    console.print(f"\n[bold yellow]Reproducibility Score:[/bold yellow] {score:.1f}/10\n")

    # Breakdown Table
    breakdown_table = Table(title="Breakdown")
    breakdown_table.add_column("Category", style="bold")
    breakdown_table.add_column("Result")

    for key, value in breakdown.items():
        color = "green" if value == "GOOD" else "red"
        breakdown_table.add_row(key, f"[{color}]{value}[/{color}]")

    console.print(breakdown_table)


if __name__ == "__main__":
    main()