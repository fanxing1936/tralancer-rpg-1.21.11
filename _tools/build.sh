#!/bin/sh
# Rebuild the upgraded pack from the pristine 1.21 copy in _orig/.
set -e
cd "$(dirname "$0")"
rm -rf ../rpg
cp -r ../_orig ../rpg
echo "== 1. version migration 1.21 -> 1.21.11 =="
python migrate.py   ../rpg
echo
echo "== 2. tick-path optimisation =="
python optimize.py  ../rpg
python opt_spawn.py ../rpg
# 变种召唤的滚雪球：召出来的变种没打已处理标记，下一刻又被重掷一遍
python opt_cascade.py ../rpg
python opt_misc.py  ../rpg
python add_items.py ../resourcepack ../rpg
python add_skills.py ../rpg
python add_twins.py  ../resourcepack ../rpg
python add_lucifer.py ../resourcepack ../rpg
python add_leviathan.py ../resourcepack ../rpg
python add_runes.py ../rpg ../resourcepack
python add_epics.py ../resourcepack ../rpg
python add_exorcism.py ../rpg
python add_pact.py ../rpg
python add_squad.py ../rpg
python retype_longinus.py ../resourcepack ../rpg
python make_boxes.py ../rpg
# 上面这些生成器同样会往 ../resourcepack 写手持变换，而它们写的是作者
# 原本的非等比缩放。rp_build.sh 末尾跑 fix_display 就是为了这个 ——
# 这里不跑，单独重建数据包就会把刀刃的剪切和副手反握又装回去。
python fix_display.py ../resourcepack
echo
echo "== 2b. guard the empty-tag entity walks =="
# 多人适配：单人下看不出来的归属错、全局标签互踩，以及按人数放大的遍历
python opt_mp.py ../rpg
python opt_index.py ../rpg
python opt_type.py ../rpg
python opt_guard.py ../rpg
# 把与 @s 无关的存在性判定从 as @e 循环里提出来（O(n²) -> O(n)）
python opt_hoist.py ../rpg
python opt_invert.py ../rpg
echo
echo "== 3. validation =="
python validate.py  ../rpg
echo
echo "== 4. per-tick profile =="
python profile_tick.py ../rpg
