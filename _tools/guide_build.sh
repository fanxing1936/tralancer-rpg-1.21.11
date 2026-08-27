#!/bin/sh
# Regenerate the codex from pack item / loot data and reviewed system JSON
# (_pact.json, _squad.json, _divine.json, _campaign_beelzebub.json).
set -e
cd "$(dirname "$0")"
python extract_items.py   ../rpg
python extract_loot.py    ../rpg
python build_guide.py
python build_loot_frag.py
python write_debug_commands.py
python emit_guide.py
python check_debug_commands.py
python check_beelzebub_campaign_docs.py
python check_beelzebub_campaign_config.py ../rpg --require-wired
python check_beelzebub_narrative_ui.py ../rpg --story-contract
python check_endless_exorcism_docs.py
python check_prayer_supplies.py ../rpg --docs
python unused_textures.py ../resourcepack | head -3
echo "wrote ../TRALANCER-RPG-图鉴.html"
