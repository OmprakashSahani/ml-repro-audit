from ml_audit.github_api import fetch_file_content


def analyze_code_quality(owner: str, repo: str, files: list[str]) -> dict:
    quality = {
        "has_pinned_dependencies": False,
        "has_seed_control": False,
        "has_training_loop": False,
        "has_config_files": False,
    }

    for file_path in files:
        path = file_path.lower()

        if path in {"requirements.txt", "pyproject.toml"}:
            content = fetch_file_content(owner, repo, file_path)

            if "==" in content or ">=" in content or "~=" in content:
                quality["has_pinned_dependencies"] = True

        if path.endswith((".yaml", ".yml", ".json", ".toml")) and (
            "config" in path or "configs/" in path
        ):
            quality["has_config_files"] = True

    python_files = [f for f in files if f.endswith(".py")][:20]

    for file_path in python_files:
        content = fetch_file_content(owner, repo, file_path).lower()

        if not content:
            continue

        if (
            "manual_seed" in content
            or "np.random.seed" in content
            or "random.seed" in content
        ):
            quality["has_seed_control"] = True

        if "for epoch" in content or "loss.backward" in content or ".backward()" in content:
            quality["has_training_loop"] = True

    return quality
