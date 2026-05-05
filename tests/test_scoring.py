from ml_audit.scoring import compute_reproducibility_score, compute_risk_level


def test_compute_reproducibility_score_full():
    analysis = {
        "has_readme": True,
        "has_license": True,
        "has_pyproject": True,
        "has_requirements": False,
        "has_tests": True,
        "has_examples": True,
        "has_ci": True,
        "has_benchmarks": True,
        "has_dataset_docs": True,
    }

    score, breakdown = compute_reproducibility_score(analysis)

    assert score == 10.0
    assert breakdown["environment_setup"] == "GOOD"
    assert breakdown["ci_cd"] == "GOOD"
    assert breakdown["benchmarks"] == "GOOD"


def test_compute_risk_level():
    assert compute_risk_level(9.0) == "LOW"
    assert compute_risk_level(6.0) == "MEDIUM"
    assert compute_risk_level(3.0) == "HIGH"