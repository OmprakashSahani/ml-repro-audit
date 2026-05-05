def detect_ml_patterns(files: list[str]) -> dict:
    patterns = {
        "uses_pytorch": False,
        "uses_distributed": False,
        "uses_all_reduce": False,
        "uses_dataparallel": False,
    }

    for file_path in files:
        if not file_path.endswith(".py"):
            continue

        path = file_path.lower()

        if "torch" in path:
            patterns["uses_pytorch"] = True

        if "distributed" in path:
            patterns["uses_distributed"] = True

        if "all_reduce" in path:
            patterns["uses_all_reduce"] = True

        if "dataparallel" in path or "data_parallel" in path:
            patterns["uses_dataparallel"] = True

    return patterns