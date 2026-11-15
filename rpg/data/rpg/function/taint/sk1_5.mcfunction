# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/1_5
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m5
# 王座回绝 —— 靠得太近的人会被王座本身拒斥。
playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 0.55
particle end_rod ~ ~1.5 ~ 2.5 1.2 2.5 0.08 72
particle enchanted_hit ~ ~1 ~ 3 1 3 0.15 64
execute as @e[tag=rpg.unit.f,distance=..6] at @s run function rpg:taint/sk1e_reject
# Lucifer mesh appearance (add_lucifer_model.py)
execute if entity @s[tag=rpg.lu,tag=!rpg.lu.phase2] run function rpg:lucifer_lord/skill/sk1_5
