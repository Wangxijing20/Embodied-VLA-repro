# Embodied-VLA-repro

Reproducible VLA/Embodied AI reproduction repo (Tsinghua).  
Focus: data → training/finetuning → evaluation → deployment, with clear experiment logs.

## Repo Structure
- `0_readme/` : checklists & templates (how to reproduce, how to log)
- `1_papers/` : paper list + reading notes
- `2_repro/` : reproduction code skeleton (configs/scripts/common utils)
- `3_experiments/` : run logs, results, and comparisons
- `4_assets/` : figures, demo gifs, slides, etc.

## How I Work (Repro Protocol)
1) Select a target paper + define scope  
2) Implement minimal runnable pipeline  
3) Match metrics / ablate key components  
4) Document deviations + commit evidence (configs, logs, results)

## Current Status
- Repo initialized ✅
- SSH push verified ✅
- Next: add reproducible run template under `2_repro/` (configs + scripts)
