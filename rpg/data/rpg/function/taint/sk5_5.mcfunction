# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/5_5
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m25
# 怒潮 —— 暴怒从中心炸开，把所有人赶出他的呼吸。
playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle sweep_attack ~ ~1 ~ 3 1 3 0 26
particle crit ~ ~1 ~ 4 1 4 0.22 80
particle dust{color:[1.0,0.36,0.32],scale:2} ~ ~1 ~ 4 1 4 0.05 72
execute as @e[tag=rpg.unit.f,distance=..8] at @s run function rpg:taint/sk5e_surge
# 萨麦尔外观（add_samael_model.py）
execute if entity @s[tag=rpg.sml] run function rpg:samael_lord/skill/sk5_5
