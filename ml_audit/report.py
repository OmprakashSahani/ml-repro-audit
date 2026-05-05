def generate_insights(analysis: dict) -> list[str]:
    insights = []

    if not analysis["has_requirements"] and not analysis["has_pyproject"]:
        insights.append("Missing dependency specification → environment not reproducible")

    if not analysis["has_tests"]:
        insights.append("No tests detected → reliability risk")

    if not analysis["has_examples"]:
        insights.append("No usage examples → harder to validate results")

    if not analysis["has_readme"]:
        insights.append("Missing README → poor documentation")

    if analysis["has_pyproject"]:
        insights.append("Modern Python packaging detected → good practice")

    return insights