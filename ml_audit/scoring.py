def compute_reproducibility_score(analysis: dict) -> tuple[float, dict]:
    """
    Compute reproducibility score based on repository structure signals.
    """

    score = 0
    breakdown = {}

    if analysis["has_pyproject"] or analysis["has_requirements"]:
        score += 2
        breakdown["environment_setup"] = "GOOD"
    else:
        breakdown["environment_setup"] = "MISSING"

    if analysis["has_readme"]:
        score += 2
        breakdown["documentation"] = "GOOD"
    else:
        breakdown["documentation"] = "MISSING"

    if analysis["has_tests"]:
        score += 2
        breakdown["tests"] = "GOOD"
    else:
        breakdown["tests"] = "MISSING"

    if analysis["has_examples"]:
        score += 2
        breakdown["examples"] = "GOOD"
    else:
        breakdown["examples"] = "MISSING"

    if analysis["has_license"]:
        score += 2
        breakdown["license"] = "GOOD"
    else:
        breakdown["license"] = "MISSING"

    return float(score), breakdown


def compute_risk_level(score: float) -> str:
    """
    Determine risk level based on reproducibility score.
    """

    if score >= 8:
        return "LOW"
    elif score >= 5:
        return "MEDIUM"
    else:
        return "HIGH"