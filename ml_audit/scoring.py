def compute_reproducibility_score(analysis: dict) -> tuple[float, dict]:
    score = 0.0
    breakdown = {}

    if analysis["has_pyproject"] or analysis["has_requirements"]:
        score += 2.0
        breakdown["environment_setup"] = "GOOD"
    else:
        breakdown["environment_setup"] = "MISSING"

    if analysis["has_readme"]:
        score += 1.5
        breakdown["documentation"] = "GOOD"
    else:
        breakdown["documentation"] = "MISSING"

    if analysis["has_tests"]:
        score += 1.5
        breakdown["tests"] = "GOOD"
    else:
        breakdown["tests"] = "MISSING"

    if analysis["has_examples"]:
        score += 1.0
        breakdown["examples"] = "GOOD"
    else:
        breakdown["examples"] = "MISSING"

    if analysis["has_license"]:
        score += 1.0
        breakdown["license"] = "GOOD"
    else:
        breakdown["license"] = "MISSING"

    if analysis["has_ci"]:
        score += 1.0
        breakdown["ci_cd"] = "GOOD"
    else:
        breakdown["ci_cd"] = "MISSING"

    if analysis["has_benchmarks"]:
        score += 1.0
        breakdown["benchmarks"] = "GOOD"
    else:
        breakdown["benchmarks"] = "MISSING"

    if analysis["has_dataset_docs"]:
        score += 1.0
        breakdown["dataset_documentation"] = "GOOD"
    else:
        breakdown["dataset_documentation"] = "MISSING"

    return min(score, 10.0), breakdown


def compute_risk_level(score: float) -> str:
    if score >= 8:
        return "LOW"
    elif score >= 5:
        return "MEDIUM"
    else:
        return "HIGH"