def compute_reproducibility_score(analysis: dict) -> tuple[float, dict]:
    """
    Compute reproducibility score based on repository structure signals.
    """

    score = 0
    breakdown = {}

    # Config / dependency management
    if analysis["has_pyproject"] or analysis["has_requirements"]:
        score += 2
        breakdown["environment_setup"] = "GOOD"
    else:
        breakdown["environment_setup"] = "MISSING"

    # Documentation
    if analysis["has_readme"]:
        score += 2
        breakdown["documentation"] = "GOOD"
    else:
        breakdown["documentation"] = "MISSING"

    # Tests
    if analysis["has_tests"]:
        score += 2
        breakdown["tests"] = "GOOD"
    else:
        breakdown["tests"] = "MISSING"

    # Examples / usage
    if analysis["has_examples"]:
        score += 2
        breakdown["examples"] = "GOOD"
    else:
        breakdown["examples"] = "MISSING"

    # License (important for reuse)
    if analysis["has_license"]:
        score += 2
        breakdown["license"] = "GOOD"
    else:
        breakdown["license"] = "MISSING"

    final_score = score / 10 * 10  # normalize to /10

    return final_score, breakdown
