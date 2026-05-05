from ml_audit.github_api import fetch_file_content


def detect_ml_patterns(owner: str, repo: str, files: list[str]) -> dict:
    patterns = {
        "uses_pytorch": False,
        "uses_distributed": False,
        "uses_all_reduce": False,
        "uses_dataparallel": False,
    }

    python_files = [file_path for file_path in files if file_path.endswith(".py")][:10]

    for file_path in python_files:
        content = fetch_file_content(owner, repo, file_path)

        if not content:
            continue

        text = content.lower()

        if "import torch" in text or "from torch" in text:
            patterns["uses_pytorch"] = True

        if "torch.distributed" in text or "distributeddataParallel".lower() in text:
            patterns["uses_distributed"] = True

        if "all_reduce" in text:
            patterns["uses_all_reduce"] = True

        if "dataparallel" in text or "distributeddataparallel" in text:
            patterns["uses_dataparallel"] = True

    return patterns