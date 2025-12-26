# 2_repro — Reproducible Runner Skeleton

This folder contains a minimal, reproducible runner:
- single entry: `run.py`
- config-driven: `configs/base.yaml`
- outputs (logs/results) are written to `3_experiments/`

## Quick Start (CPU)
```bash
pip install -r requirements.txt
python run.py --config configs/base.yaml

What this demonstrates (for recruiters)
clean entry point + config management
deterministic run (seed)
structured outputs: metrics + run metadata
easy to extend to any VLA/embodied paper reproduction