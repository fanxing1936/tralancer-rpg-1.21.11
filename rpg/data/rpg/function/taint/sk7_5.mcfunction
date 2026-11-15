# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/7_5
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m35
# 金牢 —— 黄金不是奖赏，是把脚钉在账本上的铆钉。
playsound minecraft:block.anvil.land hostile @a[distance=..32] ~ ~ ~ 0.8 1.35
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.75
particle end_rod ~ ~1 ~ 3 1 3 0.08 72
particle wax_on ~ ~0.5 ~ 3 0.5 3 0.12 80
execute as @e[tag=rpg.unit.f,distance=..7] run function rpg:taint/sk7e_prison
# 玛门外观（add_mammon_model.py）
execute if entity @s[tag=rpg.mml] run function rpg:mammon_lord/skill/sk7_5
