#!/usr/bin/env python3
"""Tests for bin/game-scene that need no display. Arcade detection is skipped when mame or the sample ROMs are absent.

  python3 dev/test_game_scene.py            (set ASCIISCAPE_TEST_ROMS=dir to also test against real ROMs)
"""
import importlib.machinery
import importlib.util
import os
import re
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
loader = importlib.machinery.SourceFileLoader("game_scene", str(ROOT / "bin/game-scene"))
gs = importlib.util.module_from_spec(importlib.util.spec_from_loader("game_scene", loader))
loader.exec_module(gs)


def screens(layout):
    return [tuple(map(int, m)) for m in re.findall(r'<screen index="0"><bounds x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)"', layout)]


class Layout(unittest.TestCase):
    def test_matches_hand_made_dkong(self):  # the layout this generator replaced
        self.assertEqual(screens(gs.mame_layout(3 / 4, 16 / 9))[-1], (555, 0, 810, 1080))

    def test_main_screen_is_last_so_it_draws_on_top(self):
        for ga, sa in [(4 / 3, 16 / 9), (3 / 4, 32 / 9), (4 / 3, 5 / 4), (16 / 9, 16 / 9), (3 / 4, 9 / 16)]:
            s = screens(gs.mame_layout(ga, sa))
            W, H = round(1080 * sa), 1080
            x, y, w, h = s[-1]
            self.assertTrue(0 <= x and x + w <= W + 1 and 0 <= y and y + h <= H + 1, (ga, sa, s[-1]))

    def test_bars_are_fully_covered(self):
        for ga, sa in [(3 / 4, 32 / 9), (4 / 3, 21 / 9), (4 / 3, 16 / 9), (10 / 9, 16 / 10)]:
            s = screens(gs.mame_layout(ga, sa))
            W = round(1080 * sa)
            covered = [False] * W
            for x, _, w, _ in s:
                for i in range(max(0, x), min(W, x + w)):
                    covered[i] = True
            self.assertTrue(all(covered), (ga, sa))

    def test_letterbox_when_game_is_wider_than_screen(self):
        s = screens(gs.mame_layout(16 / 9, 4 / 3))
        self.assertTrue(len(s) > 1 and s[-1][0] == 0 and s[-1][2] == 1440)

    def test_same_aspect_has_no_bars(self):
        self.assertEqual(len(screens(gs.mame_layout(16 / 9, 16 / 9))), 1)

    def test_shader_has_aspect(self):
        self.assertIn("/ 1.333333;", gs.GLSL % {"aspect": 4 / 3, "keep": 0.32})


class Discovery(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        os.environ["ASCIISCAPE_ROMS"] = str(self.tmp / "roms")
        (self.tmp / "roms/sub").mkdir(parents=True)
        gs.CACHE_FILE = self.tmp / "cache.json"
        self.reg = gs.load_registry()

    def test_empty_and_missing_dirs(self):
        self.assertEqual(gs.discover(self.reg), {})
        shutil.rmtree(self.tmp / "roms")
        self.assertEqual(gs.discover(self.reg), {})

    def test_registry_match_by_pattern(self):
        (self.tmp / "roms/Donkey_Kong (World).zip").write_bytes(b"x")
        g = gs.discover(self.reg)["dkong"]
        self.assertEqual((g.machine, g.aspect), ("dkong", 0.75))

    def test_console_by_extension_and_in_zip(self):
        (self.tmp / "roms/sub/Some Game (USA).nes").write_bytes(b"x")
        with zipfile.ZipFile(self.tmp / "roms/Other.zip", "w") as z:
            z.writestr("other.gba", b"x")
        games = gs.discover(self.reg)
        self.assertEqual(sorted(games), ["other", "some-game"])
        self.assertEqual((games["some-game"].core, games["other"].core), ("nestopia", "mgba"))

    def test_junk_is_ignored(self):
        (self.tmp / "roms/readme.txt").write_text("hi")
        (self.tmp / "roms/.hidden.nes").write_bytes(b"x")
        (self.tmp / "roms/notazip.zip").write_bytes(b"not a zip")
        self.assertEqual(gs.discover(self.reg), {})

    def test_missing_roms_listed_only_with_all(self):
        all_ = gs.discover(self.reg, want_all=True)
        self.assertEqual(all_["dkong"].problem, "ROM not found")
        self.assertNotIn("dkong", gs.discover(self.reg))

    @unittest.skipUnless(shutil.which("mame") and os.environ.get("ASCIISCAPE_TEST_ROMS"), "needs mame and ASCIISCAPE_TEST_ROMS")
    def test_unknown_arcade_zip_is_verified_by_mame(self):
        src = Path(os.environ["ASCIISCAPE_TEST_ROMS"]) / "donkey_kong.zip"
        if not src.exists():
            self.skipTest("donkey_kong.zip not in ASCIISCAPE_TEST_ROMS")
        shutil.copy(src, self.tmp / "roms/dkong.zip")
        (self.tmp / "roms/notmame.zip").write_bytes(b"")
        info = gs.arcade_info(self.tmp / "roms/dkong.zip", str(self.tmp / "roms"), {})
        self.assertEqual(info, ("dkong", 3 / 4))
        self.assertIsNone(gs.arcade_info(self.tmp / "roms/notmame.zip", str(self.tmp / "roms"), {}))


class Commands(unittest.TestCase):
    def test_no_hardcoded_home(self):
        text = (ROOT / "bin/game-scene").read_text()
        self.assertNotIn("/home/", text)


if __name__ == "__main__":
    unittest.main()
