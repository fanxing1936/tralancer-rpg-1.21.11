#!/bin/sh
# Rebuild the upgraded resource pack from the pristine 1.21 copy in _orig_rp/.
set -e
cd "$(dirname "$0")"
echo "== 1. resource pack migration 1.21 -> 1.21.11 =="
python rp_migrate.py  ../_orig_rp ../resourcepack
echo
echo "== 1b. wire up the unused weapon art =="
python import_twin_art.py ../resourcepack
python fix_art.py     ../resourcepack
python add_items.py   ../resourcepack ../rpg
python add_skills.py  ../rpg
python add_twins.py   ../resourcepack ../rpg
python add_lucifer.py ../resourcepack ../rpg
python add_leviathan.py ../resourcepack ../rpg
python add_runes.py ../rpg ../resourcepack
python add_epics.py ../resourcepack ../rpg
python retype_longinus.py ../resourcepack ../rpg
python retype_wukong.py ../resourcepack ../rpg
python build_combat_prompt_font.py ../resourcepack
# last, so every hand transform in the pack has exactly one owner
python fix_display.py ../resourcepack
echo
echo "== 2. validation against the real 1.21.11 client jar =="
python rp_validate.py ../resourcepack
