# 随机召一名圣卫（塔卫、重盾、术士三选一），带 rpg.hg。由 add_holy_guards.py 生成。
execute store result score #r rpg_rg_v run random value 0..2
execute if score #r rpg_rg_v matches 0 run return run function rpg:tower_guard/summon
execute if score #r rpg_rg_v matches 1 run return run function rpg:royal_guard/summon
function rpg:end_illager/summon
