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
# Minecraft Dungeons 原作武器：坟墓克星、竖琴弩（[传说]，圣殿大团长雅克的武器）。
# 同米迦勒：早于 opt_index、make_boxes、polish_ui 与 polish_vfx。
python add_dungeons_weapons.py ../resourcepack ../rpg
python add_forge.py ../resourcepack --rp-only
python build_combat_prompt_font.py ../resourcepack
# 圣卫（塔卫）与别西卜：从 *_ref/*.bbmodel 生成部件模型、图集与音效（sounds.json）
python add_tower_guard.py ../resourcepack ../rpg
# 圣卫的另外两种：重盾（原作皇家卫兵）、术士（原作终末灾厄村民，唤魔者网格褐袍）；rpg:holy_guard/summon 三选一
python add_holy_guards.py ../resourcepack ../rpg
python add_prime_enchanter_model.py ../resourcepack ../rpg
python add_pope_model.py ../resourcepack ../rpg
python add_beelzebub.py ../resourcepack ../rpg
python add_vanguard.py ../resourcepack ../rpg
python add_leviathan_model.py ../resourcepack ../rpg
# 玛门（第七柱）外观：猪灵商人，原作模型（mammon_lord_dungeons_ref/）
python add_mammon_model.py ../resourcepack ../rpg
# 萨麦尔（第五柱）：红石巨怪；贝利尔（第六柱）：腐化坩埚；三位领主的罪仆（共用 lord_look.py / servant_look.py）
python add_samael_model.py ../resourcepack ../rpg
python add_belial_model.py ../resourcepack ../rpg
python add_lord_servants.py ../resourcepack ../rpg
# 篡夺者一阶段外观：附魔师（usurper_dungeons_ref/）
python add_usurper_model.py ../resourcepack ../rpg
# 圣殿大团长雅克：原作玩家英雄网格 + 赫克斯皮肤 + 英雄铠甲，坟墓克星与竖琴弩（jacques_dungeons_ref/）
python add_jacques_model.py ../resourcepack ../rpg
# 疯人王扫罗：原作玩家英雄网格 + 织网者皮肤 + 坚毅铠甲，千刀（saul_dungeons_ref/、saul_ghost_dungeons_ref/）
python add_saul_model.py ../resourcepack ../rpg
# 米迦勒灵体：原版 Cloudwatcher、霜冻护甲和双持武器及动作。
python add_michael_spirit_model.py ../resourcepack ../rpg
# 天使长米迦勒：半透明灵体 + 六翼（michael_dungeons_ref/，build_michael_model.py）；守望者（watchling_dungeons_ref/）
python add_michael_model.py ../resourcepack ../rpg
# 篡夺者战的特效素材：原作附魔台符文、灵魂图腾法阵、六芒星、唤魔者尖牙（usurper_fx_ref/）
python add_usurper_fx_art.py ../resourcepack
# 篡夺者二阶段外观：首席附魔师的冰电改篡夺白金，帽顶加原作王冠（须在上面两步之后）
python add_usurper_holy_look.py ../resourcepack
python add_lucifer_model.py ../resourcepack ../rpg --defer-shaders
python add_lucifer_p2_model.py ../resourcepack ../rpg
# 原作 Abomination Vine：缠枝破土的藤蔓（dungeons_conversion/generic.py 转换）
python add_lucifer_vine_model.py ../resourcepack ../rpg
python add_lucifer_model.py ../resourcepack ../rpg --finalize-shaders
python add_sunken_skeleton.py ../resourcepack ../rpg
python add_abaddon_model.py ../resourcepack ../rpg
python add_tower_wraith.py ../resourcepack ../rpg
python add_heart_of_ender.py ../resourcepack ../rpg
python add_arch_visage.py ../resourcepack ../rpg
# 教皇战特效贴图：母图在 pope_fx_ref/raw/（Codex 绘制），这里定网格和色板
python add_pope_fx_art.py ../resourcepack
# 路西法二阶段特效贴图：母图在 lucifer_p2_fx_ref/（Codex 绘制），这里定网格和色板
python add_lucifer_p2_fx_art.py ../resourcepack
# 原作静态道具：毒刺弹、藤臂尖根
python add_lucifer_props.py ../resourcepack
# 最终 Boss 路西法的位图血条：饰物与标题在 lucifer_boss_ref/bar/（Codex 绘制）
python add_lucifer_boss_art.py ../resourcepack
# 篡夺者的位图血条：饰物与标题在 usurper_boss_ref/bar/（占位，正式稿见 BAR-BRIEF.md）
python add_usurper_boss_art.py ../resourcepack
# 雅克的位图血条：饰物与标题在 jacques_boss_ref/bar/（占位：原作图标与哥特字体）
python add_jacques_boss_art.py ../resourcepack
# 扫罗的位图血条：饰物与标题在 saul_boss_ref/bar/（占位：原作图标与哥特字体）
python add_saul_boss_art.py ../resourcepack
# 米迦勒的位图血条、羽毛与骨头的物品模型（占位在 michael_boss_ref/bar/）
# 米迦勒专属特效贴图：原作素材 + Codex 序列帧（michael_fx_ref/），字体 rpg:michael_vfx
python add_michael_fx_art.py ../resourcepack
python add_michael_boss_art.py ../resourcepack
python add_boss_bgm.py ../resourcepack
# last, so every hand transform in the pack has exactly one owner
python fix_display.py ../resourcepack
# 物品贴图按原生网格存储（整数倍放大的无损还原，新约按 D6 重建）
python fix_texture_grid.py ../resourcepack
echo
echo "== 2. validation against the real 1.21.11 client jar =="
python rp_validate.py ../resourcepack
