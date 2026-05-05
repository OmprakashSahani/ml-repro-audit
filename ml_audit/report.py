def generate_insights(analysis: dict) -> list[str]:
    insights = []

    if not analysis["has_requirements"] and not analysis["has_pyproject"]:
        insights.append("Missing dependency specification → environment not reproducible")

    if not analysis["has_ci"]:
        insights.append("No CI/CD detected → changes are not automatically validated")

    if not analysis["has_tests"]:
        insights.append("No tests detected → reliability risk")

    if not analysis["has_benchmarks"]:
        insights.append("No benchmarks detected → performance claims are hard to verify")

    if not analysis["has_dataset_docs"]:
        insights.append("No dataset documentation detected → experiments may be hard to reproduce")

    if not analysis["has_examples"]:
        insights.append("No usage examples → harder to validate results")

    if not analysis["has_readme"]:
        insights.append("Missing README → poor documentation")

    if analysis["has_pyproject"]:
        insights.append("Modern Python packaging detected → good practice")

    return insights