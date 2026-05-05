def compute_reproducibility_score(
    analysis: dict,
    quality: dict | None = None,
) -> tuple[float, dict]:
    quality = quality or {}

    score = 0.0
    breakdown = {}

    if analysis["has_pyproject"] or analysis["has_requirements"]:
        score += 1.5
        breakdown["environment_setup"] = "GOOD"
    else:
        breakdown["environment_setup"] = "MISSING"

    if quality.get("has_pinned_dependencies"):
        score += 1.0
        breakdown["pinned_dependencies"] = "GOOD"
    else:
        breakdown["pinned_dependencies"] = "MISSING"

    if quality.get("has_seed_control"):
        score += 1.0
        breakdown["determinism"] = "GOOD"
    else:
        breakdown["determinism"] = "MISSING"

    if analysis["has_readme"]:
        score += 1.0
        breakdown["documentation"] = "GOOD"
    else:
        breakdown["documentation"] = "MISSING"

    if analysis["has_tests"]:
        score += 1.0
        breakdown["tests"] = "GOOD"
    else:
        breakdown["tests"] = "MISSING"

    if analysis["has_examples"]:
        score += 0.75
        breakdown["examples"] = "GOOD"
    else:
        breakdown["examples"] = "MISSING"

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
        score += 0.75
        breakdown["dataset_documentation"] = "GOOD"
    else:
        breakdown["dataset_documentation"] = "MISSING"

    if quality.get("has_config_files"):
        score += 0.5
        breakdown["config_driven_runs"] = "GOOD"
    else:
        breakdown["config_driven_runs"] = "MISSING"

    if analysis["has_license"]:
        score += 0.5
        breakdown["license"] = "GOOD"
    else:
        breakdown["license"] = "MISSING"

    return min(score, 10.0), breakdown


def compute_risk_level(score: float) -> str:
    if score >= 8:
        return "LOW"
    elif score >= 5:
        return "MEDIUM"
    else:
        return "HIGH"