# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/6_2
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m27
# 迷乱 —— 你分不清哪边是他。
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle portal ~ ~1 ~ 3 1 3 0.6 80
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk6b_daze
# 贝利尔外观（add_belial_model.py）
execute if entity @s[tag=rpg.bll] run function rpg:belial_lord/skill/sk6_2
