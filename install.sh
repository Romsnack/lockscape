#!/bin/bash
# Install lockscape: symlink the programs into ~/.local/bin, create the ROM folder, report what is missing.
#
#   ./install.sh                  install into ~/.local/bin
#   ./install.sh --prefix DIR     install into DIR instead
#   ./install.sh --dry-run        only say what would happen
#   ./install.sh --force          replace existing files that are not our symlinks (they are kept as NAME.bak)
#   ./install.sh --uninstall      remove our symlinks again
#
# The programs are symlinks into this checkout, so keep the checkout where it is (git pull updates everything).

set -eu
here=$(dirname "$(readlink -f "$0")")
prefix="$HOME/.local/bin"
dry=0 force=0 uninstall=0
while [ $# -gt 0 ]; do
    case "$1" in
        --prefix) prefix=${2:?--prefix needs a directory}; shift ;;
        --dry-run) dry=1 ;;
        --force) force=1 ;;
        --uninstall) uninstall=1 ;;
        -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "install.sh: unknown option $1" >&2; exit 2 ;;
    esac
    shift
done

run() { if [ "$dry" = 1 ]; then echo "would: $*"; else "$@"; fi; }
progs="lockscape lockscape-lock lockscape-game"

if [ "$uninstall" = 1 ]; then
    for p in $progs; do
        if [ -L "$prefix/$p" ] && [ "$(readlink -f "$prefix/$p")" = "$here/bin/$p" ]; then
            run rm "$prefix/$p"; echo "removed $prefix/$p"
        fi
    done
    echo "Left alone: your ROMs, ~/.config/lockscape and ~/.local/state/lockscape."
    exit 0
fi

# -- programs ---------------------------------------------------------------
run mkdir -p "$prefix"
for p in $progs; do
    src="$here/bin/$p" dst="$prefix/$p"
    if [ -L "$dst" ] && [ "$(readlink -f "$dst")" = "$src" ]; then
        echo "ok       $dst"
    elif [ -e "$dst" ] || [ -L "$dst" ]; then
        if [ "$force" = 1 ]; then
            run mv "$dst" "$dst.bak"; run ln -s "$src" "$dst"; echo "replaced $dst (old one kept as $p.bak)"
        else
            echo "SKIPPED  $dst exists and is not ours (use --force to replace it, the old one is kept as $p.bak)"
        fi
    else
        run ln -s "$src" "$dst"; echo "linked   $dst"
    fi
done
case ":$PATH:" in *":$prefix:"*) ;; *) echo "note: $prefix is not in your PATH" ;; esac

# -- ROM folder ---------------------------------------------------------------
roms="${LOCKSCAPE_ROMS:-${XDG_DATA_HOME:-$HOME/.local/share}/lockscape/roms}"
roms=${roms%%:*}
[ -d "$roms" ] || { run mkdir -p "$roms"; echo "created  $roms  (put your own ROMs here, see roms/README.md)"; }

# -- what is there ------------------------------------------------------------------
echo
echo "Checking what is installed:"
have() { command -v "$1" >/dev/null 2>&1; }
check() {  # check COMMAND "what it is for" required|optional
    if have "$1"; then printf '  ok       %s\n' "$1"
    else printf '  %-8s %s: %s\n' "$3" "$1" "$2"; fi
}
check python3 "runs everything (3.11 or newer)" REQUIRED
python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null || echo "  REQUIRED python3 is older than 3.11 (lockscape-game needs tomllib)"
check foot "terminal that shows the animations" "for the lock screen"
check swaylock-plugin "locker that can run a program as its background" "for the lock screen"
check windowtolayer "turns a window into a lock-screen background (build it with cargo, see README)" "for the lock screen"
check mame "plays arcade games and Mega Drive / Genesis ROMs" optional
check retroarch "plays SNES, NES, Game Boy... ROMs through libretro cores" optional
check chrt "runs games at idle CPU priority" optional
echo
"$here/bin/lockscape-game" --list --all 2>/dev/null | sed 's/^/  /' | head -20 || true
echo
echo "Try it:   lockscape                 (q quits, n jumps to the next scene)"
echo "          lockscape --list          (every scene)"
echo "          lockscape-game --list          (games found in your ROM folder)"
echo "Lock:     lockscape-lock                 (see README.md for hooking it to swayidle)"
