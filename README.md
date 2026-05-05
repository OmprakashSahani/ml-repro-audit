<div align="center">

# ML Reproducibility Auditor
### A systems-oriented CLI tool to evaluate machine learning repositories for reproducibility, engineering quality, and ML infrastructure signals.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Interface](https://img.shields.io/badge/Interface-CLI-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![PyPI](https://img.shields.io/pypi/v/ml-repro-audit)
![Downloads](https://img.shields.io/pypi/dm/ml-repro-audit)

</div>

---

## Quick Demo

[![asciicast](https://asciinema.org/a/9nPj0yPcWiEqekck.svg)](https://asciinema.org/a/9nPj0yPcWiEqekck)

## Try in 10 seconds

```bash
pip install ml-repro-audit

ml-audit https://github.com/pytorch/pytorch
ml-audit https://github.com/huggingface/transformers
ml-audit https://github.com/Lightning-AI/lightning
```

---

## Motivation

Most machine learning repositories:

- Cannot be reliably reproduced
- Lack dependency and environment clarity
- Provide no benchmark guarantees
- Hide system-level bottlenecks

This tool evaluates repositories through a **systems lens**, focusing on:

- Reproducibility signals
- Engineering maturity
- ML systems design patterns

---

## Why this tool

- Goes beyond linting → evaluates ML systems signals
- Detects determinism, CI/CD, benchmarking, datasets
- Uses GitHub API (no cloning required)
- Works as CLI + GitHub Action + PyPI package

---

## Installation

```bash
pip install -e .
```

---

## Usage

```bash
ml-audit https://github.com/user/repo
```

---

## GitHub Action Usage

```yaml
name: ML Reproducibility Audit
on:
  pull_request:
  workflow_dispatch:
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: uses: OmprakashSahani/ml-repro-audit/.github/actions/ml-audit@v1.1
        with:
          repo-url: https://github.com/user/repo
```

---

## Example Script

Run a quick audit using:

```bash
./examples/run_audit.sh
```

---

## JSON Output

```bash
ml-audit https://github.com/user/repo --json
```

---

## Example Output

```text
Repository: user/repo

Structure Analysis:
- has_readme: YES
- has_license: YES
- has_ci: NO
- has_benchmarks: YES

Reproducibility Score: 7.5/10
Risk Level: MEDIUM

Code Quality Signals:
- has_pinned_dependencies: YES
- has_seed_control: NO
- has_training_loop: YES

ML Systems Detection:
- uses_pytorch: YES
- uses_distributed: YES
- uses_all_reduce: YES

Insights:
- No CI/CD detected → changes are not automatically validated
- Missing seed control → results may not be reproducible
```

---

## JSON Output Example

```json
{
  "repository": "user/repo",
  "score": 7.5,
  "risk": "MEDIUM",
  "analysis": {},
  "quality": {},
  "patterns": {},
  "insights": []
}
```

---

## Features

- GitHub API integration (with authentication support)
- Repository structure analysis (CI/CD, benchmarks, datasets)
- Code quality analysis (dependencies, determinism, training loops)
- Reproducibility scoring with weighted signals
- Risk classification (LOW / MEDIUM / HIGH)
- ML systems pattern detection (PyTorch, distributed training, all-reduce)
- Code-level inspection via GitHub API
- Insight generation based on system signals
- JSON output for automation and pipelines
- Rich CLI interface (tables, colors)

---

## GitHub Integration

This tool integrates directly with the GitHub API to:

- Fetch repository metadata and file structure
- Inspect source code for ML system patterns
- Analyze engineering signals across repositories

It is designed as a developer tool to audit and improve repository quality within the GitHub ecosystem.

---

## Use Cases

- Evaluate reproducibility of ML repositories before use
- Audit open-source projects for engineering quality
- Compare ML infrastructure practices across repositories
- Integrate into CI pipelines for repository validation

---

## Architecture

```mermaid
flowchart TD
    A[CLI Input] --> B[GitHub API]
    B --> C[File Fetcher]
    C --> D[Structure Analyzer]
    C --> E[Code Quality Analyzer]
    C --> F[ML Pattern Detector]
    D --> G[Scoring Engine]
    E --> G
    G --> H[Risk Classifier]
    D --> I[Insights Generator]
    E --> I
    F --> I
    H --> J[Report Output]
    I --> J
```

---

## Design Principles

- **Reproducibility-first** — treat environment and determinism as first-class concerns
- **Signal over noise** — focus on high-impact engineering indicators
- **System-aware analysis** — go beyond files into behavior and patterns
- **Composable design** — CLI + JSON for integration into workflows

---

## Evaluation Dimensions

The scoring system considers:

- Environment setup (dependencies, packaging)
- Determinism (seed control)
- Documentation
- Testing and validation
- CI/CD pipelines
- Benchmarking practices
- Dataset reproducibility
- Configuration-driven experimentation

---

## Roadmap

- [ ] AST-based static analysis (deeper code understanding)
- [ ] Dataset pipeline validation
- [ ] Training loop structure detection
- [ ] Performance bottleneck hints
- [ ] Multi-repo comparison
- [ ] Web dashboard (FastAPI)

---

## Limitations

- Heuristic-based detection (not full static analysis yet)
- Partial file sampling for performance
- GitHub API rate limits without authentication
- Static analysis only (does not execute code)

---

## Why This Matters

Reproducibility is a major gap in real-world ML systems.

This project explores how:

- System design decisions affect reproducibility
- Engineering practices impact reliability
- Scalability constraints influence outcomes

---

<div align="center">

*Omprakash Sahani — ML Systems Engineer (Distributed Training · Optimization · Systems)*

</div>