# exp1_plan3d_mini

目标：用最小可跑的方式把一个具身/规划类任务跑通，并且产出可复现的结果记录（config + command + metrics + run_meta）。

## How to run
1) Activate venv (PowerShell):
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1

2) Run:
   python 3_experiments\exp1_plan3d_mini\run.py

## Inputs
- config: 3_experiments/exp1_plan3d_mini/config.yaml

## Expected outputs
- outputs/<run_name>_<timestamp>/
  - command.txt
  - config.yaml / config_resolved.yaml
  - metrics.json
  - run_meta.json
