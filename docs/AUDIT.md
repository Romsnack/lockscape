# Can this be shared? Audit of every scene

Checked 2026-10-09 before the first release. "Shareable" means: no third-party code or assets copied in, nothing
personal, and the remaining risk is only about names. All art is drawn with text characters by this project.

## Code and licence

- All code is original except the points under *Needs a credit* below. The project is MIT licensed.
- The WIP experiments contained a Pac-Man maze table adapted from pacman.js (GPL-3). It is **not** in this repo: the
  shipped Pacman scene generates its own mazes. Do not copy `scenes/pacman*.py` from old work directories back in.
- Removed on purpose: the FTL and Zelda-style ("link") scenes, whose rendering was poor.
- No ROMs, BIOS files, emulator configs, save data or MAME `nvram` are included (`roms/` is git-ignored).
- No personal data found: no home paths, usernames, e-mail addresses or tokens in the sources.
  (Run `grep -rnE "/home/|@" bin share docs` again before publishing.)

## Needs a credit

| Scene | Issue | Done / to do |
|---|---|---|
| `donut` | Projection and lighting follow Andy Sloane's "donut math" (a1k0n.net/2011/07/20/donut-math.html); variable names match his donut.c. His page states no licence. | Credit added in code and README. For zero doubt, ask him, or rewrite the maths with your own names. |

## Names and trademarks

The scenes are homages drawn from scratch; none uses original sprites, maps, music or text dumps. The residual risk is
trademarks in names/descriptions, highest for Nintendo (known for takedowns). Verdicts:

| Scene | Verdict | Notes |
|---|---|---|
| life, brain, ants, fire, matrix, starfield, rain, snow, plasma, maze, aquarium, fireplace, packet* | shareable | Public algorithms / generic art. *`packet` imitates the look of a Cisco Packet Tracer simulation screen (own ASCII drawing, Cisco-style log lines); "Cisco" and "Packet Tracer" are Cisco marks, used descriptively. |
| pipes | shareable | Generic idea; description says "the classic pipes screensaver" without naming Microsoft. |
| donut | shareable with credit | See above. |
| maze3d | shareable | Description no longer names Windows. Uses four bright colours for a logo-like polyhedron; they are plain colours, not a copy. |
| tetris | shareable, small risk | "Tetris" is a trademark of The Tetris Company (the game rules are not protectable). Rename to e.g. `blocks` if you want zero risk. |
| pacman | shareable, small risk | "Pac-Man", ghost names and the dot/ghost behaviour tables are Bandai Namco's. Behaviour rules are public documentation; no assets copied. Rename (e.g. `maze-chase`) for zero risk. |
| tron | shareable, small risk | "Tron" is Disney's; light-cycle games are generic. |
| oregon | shareable, small risk | "The Oregon Trail" is a trademark; the scene uses its own drawings and phrases evoking it. |
| meatboy | shareable, small risk | "Meat Boy" is Team Meat's. Own art and level. Rename (e.g. `meatcube`) if you prefer. |
| critters | shareable | Was `pokemon`: trademarked strings (POKé BALL, POKéDEX, POKéMON) and the name are replaced; the creatures were already invented. |

Not covered by this audit: whether your ROMs are legal where you live. The project ships none and does not help find any.
