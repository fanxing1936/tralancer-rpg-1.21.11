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
# 米迦勒脊骨／肋骨：[神圣] 双持圣骸。要在 add_twins 之后（借它的副手索引块），
# 早于 opt_index、make_boxes、polish_ui 与 polish_vfx。
python add_michael.py ../resourcepack ../rpg
python build_combat_prompt_font.py ../resourcepack
# 圣卫（塔卫）与别西卜：从 *_ref/*.bbmodel 生成部件模型、图集与音效（sounds.json）
python add_tower_guard.py ../resourcepack ../rpg
python add_beelzebub.py ../resourcepack ../rpg
python add_vanguard.py ../resourcepack ../rpg
python add_leviathan_model.py ../resourcepack ../rpg
python add_sunken_skeleton.py ../resourcepack ../rpg
python add_abaddon_model.py ../resourcepack ../rpg
python add_tower_wraith.py ../resourcepack ../rpg
# last, so every hand transform in the pack has exactly one owner
python fix_display.py ../resourcepack
# 物品贴图按原生网格存储（整数倍放大的无损还原，新约按 D6 重建）
python fix_texture_grid.py ../resourcepack
echo
echo "== 2. validation against the real 1.21.11 client jar =="
python rp_validate.py ../resourcepack
