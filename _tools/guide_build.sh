#!/bin/sh
# Regenerate the codex from pack item / loot data and reviewed system JSON
# (_pact.json, _squad.json, _divine.json).
set -e
cd "$(dirname "$0")"
python extract_items.py   ../rpg
python extract_loot.py    ../rpg
python build_guide.py
python build_loot_frag.py
python emit_guide.py
python unused_textures.py ../resourcepack | head -3
echo "wrote ../TRALANCER-RPG-图鉴.html"
