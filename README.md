# Embodied-VLA-repro
Reproducible reproductions for Vision-Language-Action (VLA) / Embodied AI papers.
Goal: build clean pipelines across **env → data → training/finetuning → evaluation → demo**.

## Repo Structure
- `1_papers/` paper tracker (what/why/how to reproduce)
- `2_repro/` codebases (one folder per paper/project)
- `3_experiments/` logs, configs, checkpoints pointers (no large files committed)
- `0_readme/` templates (checklists, writeups)
- `4_assets/` figures for README / docs

## Repro Policy (must be reproducible)
- Every repro has: `README`, `env.yml` or `requirements.txt`, `run.sh`, and `results.md`.
- Store large artifacts via links (cloud) and keep repo lightweight.
- Record exact commits + seeds + key metrics.

## Current Focus
- VLA + Embodied tasks (policy learning, multimodal perception, action decoding)
- Simulation-first, hardware-later (clean interface for real robots)

## Status
- [ ] Select Paper #1
- [ ] Setup baseline environment + first run
- [ ] Report metrics + failure cases

