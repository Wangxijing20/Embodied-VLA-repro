import json
import os
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml


@dataclass
class Config:
    seed: int = 42
    out_dir: str = "outputs"
    run_name: str = "quickcheck"


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def load_cfg(cfg_path: str) -> Config:
    with open(cfg_path, "r", encoding="utf-8") as f:
        d = yaml.safe_load(f) or {}
    return Config(**d)


def main():
    cfg = load_cfg("2_repro/configs/base.yaml")
    set_seed(cfg.seed)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(cfg.out_dir) / f"{cfg.run_name}_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # deterministic "metric" for quickcheck
    x = np.random.randn(1000)
    metric = float(np.mean(x))

    (run_dir / "metrics.json").write_text(json.dumps({"metric": metric}, indent=2), encoding="utf-8")
    (run_dir / "run_meta.json").write_text(
        json.dumps(
            {
                "seed": cfg.seed,
                "run_name": cfg.run_name,
                "out_dir": cfg.out_dir,
                "cwd": os.getcwd(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("OK | run_dir =", run_dir.as_posix())
    print("metric =", metric)


if __name__ == "__main__":
    main()