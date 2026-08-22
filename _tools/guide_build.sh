#!/bin/sh
# Regenerate the codex from the data pack's own item / loot / entity data.
set -e
cd "$(dirname "$0")"
python extract_items.py   ../rpg
python extract_loot.py    ../rpg
python build_guide.py
python build_loot_frag.py
python emit_guide.py
python unused_textures.py ../resourcepack | head -3
echo "wrote ../TRALANCER-RPG-图鉴.html"
