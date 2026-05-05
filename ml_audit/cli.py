import argparse
import json

from rich.console import Console
from rich.table import Table

from ml_audit.analyzer.code_quality import analyze_code_quality
from ml_audit.analyzer.ml_patterns import detect_ml_patterns
from ml_audit.analyzer.repo_structure import analyze_repo_files
from ml_audit.github_api import (
    fetch_repo_files,
    fetch_repo_metadata,
    parse_github_url,
)
from ml_audit.report import generate_insights
from ml_audit.scoring import compute_reproducibility_score, compute_risk_level


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

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
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
        quality = analyze_code_quality(owner, repo, files)
        patterns = detect_ml_patterns(owner, repo, files)

        score, breakdown = compute_reproducibility_score(analysis, quality)
        risk = compute_risk_level(score)
        insights = generate_insights(analysis)

    except ValueError as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            console.print(f"[red]Error:[/red] {e}")
        return

    if args.json:
        output = {
            "repository": metadata["full_name"],
            "stars": metadata["stargazers_count"],
            "analysis": analysis,
            "quality": quality,
            "patterns": patterns,
            "score": score,
            "risk": risk,
            "breakdown": breakdown,
            "insights": insights,
        }
        print(json.dumps(output, indent=2))
        return

    console.print(f"\n[bold cyan]Repository:[/bold cyan] {metadata['full_name']}")
    console.print(f"[bold]Stars:[/bold] {metadata['stargazers_count']}\n")

    structure_table = Table(title="Structure Analysis")
    structure_table.add_column("Check", style="bold")
    structure_table.add_column("Status")

    for key, value in analysis.items():
        status = "[green]YES[/green]" if value else "[red]NO[/red]"
        structure_table.add_row(key, status)

    console.print(structure_table)

    console.print(f"\n[bold yellow]Reproducibility Score:[/bold yellow] {score:.1f}/10")

    color = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "red",
    }[risk]

    console.print(f"[bold]Risk Level:[/bold] [{color}]{risk}[/{color}]\n")

    breakdown_table = Table(title="Breakdown")
    breakdown_table.add_column("Category", style="bold")
    breakdown_table.add_column("Result")

    for key, value in breakdown.items():
        result_color = "green" if value == "GOOD" else "red"
        breakdown_table.add_row(key, f"[{result_color}]{value}[/{result_color}]")

    console.print(breakdown_table)

    quality_table = Table(title="Code Quality Signals")
    quality_table.add_column("Signal", style="bold")
    quality_table.add_column("Detected")

    for key, value in quality.items():
        status = "[green]YES[/green]" if value else "[red]NO[/red]"
        quality_table.add_row(key, status)

    console.print(quality_table)

    pattern_table = Table(title="ML Systems Detection")
    pattern_table.add_column("Pattern", style="bold")
    pattern_table.add_column("Detected")

    for key, value in patterns.items():
        status = "[green]YES[/green]" if value else "[red]NO[/red]"
        pattern_table.add_row(key, status)

    console.print(pattern_table)

    console.print("\n[bold magenta]Insights:[/bold magenta]")

    if not insights:
        console.print("[green]No major issues detected[/green]")
    else:
        for insight in insights:
            console.print(f"- {insight}")


if __name__ == "__main__":
    main()