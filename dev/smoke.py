#!/usr/bin/env python3
"""Run every scene headlessly at several terminal sizes and report crashes and slow scenes.

  dev/smoke.py [--frames 200] [--only name,name] [--seed 1]

Exit status is 1 if any scene raises. "SLOW" means a frame takes more than half of its time budget.
"""
import argparse
import random
import sys
import time
import traceback

from _load import load

ap = argparse.ArgumentParser()
ap.add_argument("--frames", type=int, default=200)
ap.add_argument("--only", help="comma-separated scene names")
ap.add_argument("--seed", type=int, default=1)
args = ap.parse_args()

mod = load()
theme = mod.load_theme()
names = args.only.split(",") if args.only else list(mod.SCENES)
sizes = [(10, 6), (40, 12), (80, 24), (213, 56), (250, 70)]
failed = 0
for name in names:
    cls = mod.SCENES[name]
    worst = 0.0
    try:
        for w, h in sizes:
            random.seed(args.seed)
            canvas, scene = mod.Canvas(w, h, theme["surface"]), cls(w, h, theme)
            t0 = time.perf_counter()
            for _ in range(args.frames):
                canvas.clear()
                scene.draw(canvas, 1 / scene.fps)
            ms = (time.perf_counter() - t0) / args.frames * 1000
            if (w, h) == (213, 56):
                worst = ms
        slow = "SLOW" if worst > 500 / cls.fps else "ok"
        print(f"{name:<10} {slow:<5} {worst:6.1f} ms/frame at 213x56 (budget {1000 / cls.fps:.0f})")
    except Exception:
        failed += 1
        print(f"{name:<10} FAIL  at {w}x{h}")
        traceback.print_exc()
sys.exit(1 if failed else 0)
