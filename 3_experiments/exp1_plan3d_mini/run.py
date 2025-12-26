import json
import os
import random
import sys
import platform
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml


@dataclass
class Config:
    seed: int = 42
    out_dir: str = "outputs"
    run_name: str = "exp1_plan3d_mini"
    grid: dict = None
    agents: dict = None
    planner: dict = None


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def load_cfg(cfg_path: str) -> Config:
    with open(cfg_path, "r", encoding="utf-8") as f:
        d = yaml.safe_load(f) or {}
    return Config(**d)


def git_head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def dump_repro_artifacts(run_dir: Path, cfg: dict):
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "config_resolved.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (run_dir / "command.txt").write_text(
        " ".join([sys.executable] + sys.argv) + "\n",
        encoding="utf-8",
    )


# ---------- 3D A* (minimal) ----------
def neighbors_3d(x, y, z, X, Y, Z):
    for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < X and 0 <= ny < Y and 0 <= nz < Z:
            yield nx, ny, nz


def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])


def astar_3d(start, goal, occ, max_expand=200000):
    # occ: bool array [X,Y,Z] True means obstacle
    import heapq
    X, Y, Z = occ.shape
    if occ[start] or occ[goal]:
        return None

    pq = []
    heapq.heappush(pq, (manhattan(start, goal), 0, start))
    came = {start: None}
    g = {start: 0}
    expanded = 0

    while pq:
        f, cg, cur = heapq.heappop(pq)
        if cur == goal:
            # reconstruct
            path = []
            p = cur
            while p is not None:
                path.append(p)
                p = came[p]
            path.reverse()
            return path

        expanded += 1
        if expanded > max_expand:
            return None

        for nb in neighbors_3d(*cur, X, Y, Z):
            if occ[nb]:
                continue
            ng = cg + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                came[nb] = cur
                heapq.heappush(pq, (ng + manhattan(nb, goal), ng, nb))

    return None


def sample_free_cell(occ):
    X, Y, Z = occ.shape
    while True:
        c = (random.randrange(X), random.randrange(Y), random.randrange(Z))
        if not occ[c]:
            return c


def main():
    cfg_path = "3_experiments/exp1_plan3d_mini/config.yaml"
    cfg = load_cfg(cfg_path)
    set_seed(cfg.seed)

    # prepare run dir
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(cfg.out_dir) / f"{cfg.run_name}_{ts}"

    # build random 3D occupancy grid
    X, Y, Z = cfg.grid["x"], cfg.grid["y"], cfg.grid["z"]
    p = float(cfg.grid.get("obstacle_prob", 0.1))
    occ = (np.random.rand(X, Y, Z) < p)

    n = int(cfg.agents["n"])
    starts, goals = [], []
    for _ in range(n):
        s = sample_free_cell(occ)
        g = sample_free_cell(occ)
        starts.append(s)
        goals.append(g)

    # plan independently (baseline)
    paths = []
    success = 0
    total_len = 0
    max_len = 0
    for s, g in zip(starts, goals):
        path = astar_3d(s, g, occ, max_expand=int(cfg.planner.get("max_expand", 200000)))
        if path is None:
            paths.append(None)
            continue
        success += 1
        L = len(path) - 1
        total_len += L
        max_len = max(max_len, L)
        paths.append(path)

    metrics = {
        "success_rate": success / n,
        "avg_path_len": (total_len / success) if success > 0 else None,
        "makespan_len": max_len if success > 0 else None,
        "n_agents": n,
        "grid": {"x": X, "y": Y, "z": Z, "obstacle_prob": p},
    }

    cfg_dict = {
        "seed": cfg.seed,
        "out_dir": cfg.out_dir,
        "run_name": cfg.run_name,
        "grid": cfg.grid,
        "agents": cfg.agents,
        "planner": cfg.planner,
    }

    dump_repro_artifacts(run_dir, cfg_dict)

    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (run_dir / "run_meta.json").write_text(
        json.dumps(
            {
                "seed": cfg.seed,
                "run_name": cfg.run_name,
                "out_dir": cfg.out_dir,
                "cwd": os.getcwd(),
                "time": ts,
                "python": sys.version,
                "platform": platform.platform(),
                "git_commit": git_head(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("OK | run_dir =", run_dir.as_posix())
    print("metrics =", metrics)


if __name__ == "__main__":
    main()