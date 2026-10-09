#!/usr/bin/env python3
"""Test a new lockscape scene headlessly.

  python3 harness.py scenes/foo.py ClassName [--frames 300] [--png out.png] [--at SECONDS] [--size 160x45]

Loads bin/lockscape as a module, execs the scene file inside its namespace
(so Scene, Canvas, mix, gradient, make_sprite, blit, WHITE... are all available),
runs the scene at several terminal sizes, reports ms/frame, and optionally renders
one frame as a PNG (each cell 9x18 px, using the real fg/bg colours) to inspect visually.
"""
import argparse
import random
import time
from pathlib import Path

from _load import load

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("cls")
ap.add_argument("--frames", type=int, default=300)
ap.add_argument("--png")
ap.add_argument("--at", type=float, default=8.0, help="simulated seconds before the PNG snapshot")
ap.add_argument("--size", default="160x45")
ap.add_argument("--seed", type=int)
args = ap.parse_args()


def find_font():
    """A monospace font for the PNG render: $HARNESS_FONT, else the first match of fc-match."""
    import os
    import subprocess
    if os.environ.get("HARNESS_FONT"):
        return os.environ["HARNESS_FONT"]
    return subprocess.run(["fc-match", "-f", "%{file}", "monospace"], capture_output=True, text=True).stdout

mod = load()
ns = mod.__dict__
exec(compile(Path(args.file).read_text(), args.file, "exec"), ns)
cls = ns[args.cls]
theme = mod.load_theme()

for (w, h) in [(80, 24), (120, 35), (213, 56), (40, 12), (10, 6)]:
    if args.seed is not None:
        random.seed(args.seed)
    canvas = mod.Canvas(w, h, theme["surface"])
    scene = cls(w, h, theme)
    dt = 1 / scene.fps
    t0 = time.perf_counter()
    for _ in range(args.frames):
        canvas.clear()
        scene.draw(canvas, dt)
    ms = (time.perf_counter() - t0) / args.frames * 1000
    budget = 1000 / scene.fps
    print(f"{w:>4}x{h:<3} fps={scene.fps:<3} {ms:6.2f} ms/frame (budget {budget:.0f} ms) "
          f"{'OK' if ms < budget * 0.5 else 'SLOW'}")

if args.png:
    from PIL import Image, ImageDraw, ImageFont
    w, h = (int(v) for v in args.size.split("x"))
    if args.seed is not None:
        random.seed(args.seed)
    canvas = mod.Canvas(w, h, theme["surface"])
    scene = cls(w, h, theme)
    dt = 1 / scene.fps
    for _ in range(max(1, int(args.at * scene.fps))):
        canvas.clear()
        scene.draw(canvas, dt)
    cw, chh = 9, 18
    font = ImageFont.truetype(find_font(), 15)
    img = Image.new("RGB", (w * cw, h * chh))
    d = ImageDraw.Draw(img)
    for y in range(h):
        for x in range(w):
            c, f, b = canvas.ch[y][x], canvas.fg[y][x], canvas.bgc[y][x]
            d.rectangle([x * cw, y * chh, (x + 1) * cw - 1, (y + 1) * chh - 1], fill=b)
            if c == "▀":
                d.rectangle([x * cw, y * chh, (x + 1) * cw - 1, y * chh + chh // 2 - 1], fill=f)
            elif c == "▄":
                d.rectangle([x * cw, y * chh + chh // 2, (x + 1) * cw - 1, (y + 1) * chh - 1], fill=f)
            elif c == "█":
                d.rectangle([x * cw, y * chh, (x + 1) * cw - 1, (y + 1) * chh - 1], fill=f)
            elif c != " ":
                d.text((x * cw, y * chh), c, font=font, fill=f)
    img.save(args.png)
    print("wrote", args.png)
