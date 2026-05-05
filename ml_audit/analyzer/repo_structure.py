def analyze_repo_files(files: list[str]) -> dict:
    return {
        "has_readme": any(f.lower() == "readme.md" for f in files),
        "has_license": any(f.lower().startswith("license") for f in files),
        "has_pyproject": "pyproject.toml" in files,
        "has_requirements": "requirements.txt" in files,
        "has_tests": any(f.startswith("tests/") or f == "tests" for f in files),
        "has_examples": any(f.startswith("examples/") or f == "examples" for f in files),
    }