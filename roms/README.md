# Playing real games on the lock screen

asciiscape can run a real game's attract/demo mode behind the lock screen, next to its ASCII scenes. **No ROMs are
included and none are ever downloaded: you provide your own**, dumped from games you own. This folder is git-ignored.

## Setup

1. Install an emulator: `mame` (arcade, Mega Drive / Genesis) and/or `retroarch` plus libretro cores (SNES, NES, Game Boy...).
2. Put your ROM files in `~/.local/share/asciiscape/roms/` (or set `ASCIISCAPE_ROMS=/dir1:/dir2`, or add
   `roms = ["~/Games/roms"]` to `~/.config/asciiscape/games.toml`). Subfolders (two levels) are searched.
3. Check what was found:

       game-scene --list          # games with a ROM, and whether they can run
       game-scene --list --all    # also the known games that still lack a ROM

Every game found joins the lock screen's shuffle bag with the ASCII scenes, one lock at a time.
To play one on the next lock: `echo dkong >> ~/.cache/ascii-lock-next`.

## What gets recognised

| ROM | How | Notes |
|---|---|---|
| Known titles in `share/games.toml` (Donkey Kong, OutRun, Sonic 3 & Knuckles, F-Zero) | file name pattern | tested |
| Console files `.sfc .smc .nes .gb .gbc .gba .pce .a26 .a78 .md .gen .smd`, also inside a `.zip` | extension | SNES and Mega Drive tested, the rest untested |
| Any other `.zip` | MAME verifies it as an arcade romset (`mame -verifyroms`) | the zip must be named after the MAME set (`pacman.zip`); parent/BIOS sets must be in the same folder |

Arcade sets must match your MAME version (0.289 was used). A set MAME calls bad is skipped, not run broken.
Game not recognised, or wrong emulator/aspect? Add an entry to `~/.config/asciiscape/games.toml` (format in `share/games.toml`).

## What the screen does with them

- The game runs at its real aspect ratio; the leftover black bars show the game's own picture, mirrored and dimmed.
  This is generated per game and per screen (`ASCIISCAPE_SCREEN=2560x1440` or `--screen` overrides the detection).
- Sound is off, input is off, CPU priority is idle, and the emulator is paused while every screen is off (sway).
- A game only does something by itself if it has an attract mode. Games that wait on a title screen forever will just show it.
- If the emulator is missing, crashes or exits, the lock shows a normal ASCII scene instead of a black screen.

Debug a game without locking: `game-scene dkong --dry-run` prints the exact command and generated files.
