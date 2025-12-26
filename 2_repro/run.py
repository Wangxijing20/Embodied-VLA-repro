import argparse
import json
import os
import platform
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml


def try_git_commit() -> str | None:
    """Return short git commit hash if available."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return r.stdout.strip()
    except Exception:
        return None


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def deep_update(base: dict, new: dict) -> dict:
    """Recursively update dict base with dict new (in-place style, but returns base)."""
    for k, v in new.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_update(base[k], v)
        else:
            base[k] = v
    return base


def default_cfg() -> dict:
    return {
        "seed": 42,
        "out_dir": "outputs",
        "run_name": "quickcheck",
    }


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=str, default="2_repro/configs/base.yaml")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--out_dir", type=str, default=None)
    p.add_argument("--run_name", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()

    cfg = default_cfg()
    file_cfg = load_yaml(Path(args.config))
    deep_update(cfg, file_cfg)

    # CLI overrides
    if args.seed is not None:
        cfg["seed"] = args.seed
    if args.out_dir is not None:
        cfg["out_dir"] = args.out_dir
    if args.run_name is not None:
        cfg["run_name"] = args.run_name

    seed = int(cfg["seed"])
    random.seed(seed)
    np.random.seed(seed)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_root = Path(cfg["out_dir"])
    run_dir = out_root / f'{cfg["run_name"]}_{ts}'
    run_dir.mkdir(parents=True, exist_ok=True)

    # ---- 1) command.txt (exact command for reproducibility) ----
    cmd = " ".join([Path(sys.executable).name] + sys.argv)
    (run_dir / "command.txt").write_text(cmd + "\n", encoding="utf-8")

    # ---- 2) config.yaml (raw config file snapshot, if exists) ----
    cfg_path = Path(args.config)
    if cfg_path.exists():
        (run_dir / "config.yaml").write_text(cfg_path.read_text(encoding="utf-8"), encoding="utf-8")

    # ---- 3) config_resolved.yaml (final resolved config after merge/override) ----
    (run_dir / "config_resolved.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # ---- 4) run_meta.json (run metadata) ----
    run_meta = {
        "seed": seed,
        "run_name": cfg["run_name"],
        "out_dir": str(out_root),
        "cwd": os.getcwd(),
        "time": ts,
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "git_commit": try_git_commit(),
    }
    (run_dir / "run_meta.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    # ---- 5) metrics.json (dummy metric, just to prove pipeline works) ----
    metric = float(np.random.rand() / 50.0)  # stable-ish small number
    (run_dir / "metrics.json").write_text(json.dumps({"metric": metric}, indent=2), encoding="utf-8")

    print("OK | run_dir =", run_dir.as_posix())
    print("metric =", metric)


if __name__ == "__main__":
    main()