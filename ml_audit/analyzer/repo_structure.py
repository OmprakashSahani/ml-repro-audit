def analyze_repo_files(files: list[str]) -> dict:
    normalized = [file_path.lower() for file_path in files]

    return {
        "has_readme": any(f == "readme.md" for f in normalized),
        "has_license": any(f.startswith("license") for f in normalized),
        "has_pyproject": "pyproject.toml" in normalized,
        "has_requirements": "requirements.txt" in normalized,
        "has_tests": any(f.startswith("tests/") for f in normalized),
        "has_examples": any(f.startswith("examples/") for f in normalized),

        # Engineering maturity
        "has_ci": any(
            f.startswith(".github/workflows/")
            and (f.endswith(".yml") or f.endswith(".yaml"))
            for f in normalized
        ),

        # Performance / ML systems signal
        "has_benchmarks": any(
            f.startswith("benchmarks/")
            or "benchmark" in f
            for f in normalized
        ),

        # Reproducibility signal
        "has_dataset_docs": any(
            "dataset" in f
            or "data/" in f
            or "datasets/" in f
            for f in normalized
        ),
    }