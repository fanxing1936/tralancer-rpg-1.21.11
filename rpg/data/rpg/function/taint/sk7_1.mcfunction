# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/7_1
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m31
# 点金 —— 他不打你，他从你身上抽。
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..32] ~ ~ ~ 1 1.4
particle wax_on ~ ~1 ~ 3 1 3 0.1 80
particle end_rod ~ ~1 ~ 2 1 2 0.05 40
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk7_take
# 玛门外观（add_mammon_model.py）
execute if entity @s[tag=rpg.mml] run function rpg:mammon_lord/skill/sk7_1
