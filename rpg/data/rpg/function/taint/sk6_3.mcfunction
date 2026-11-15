# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/6_3
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m28
# 献身 —— 他要的从来不是你的命，是你的血。
playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust{color:[0.85,0.48,0.85],scale:2} ~ ~1 ~ 3 1 3 0.1 80
execute as @e[tag=rpg.unit.f,distance=..7] run function rpg:taint/sk6c_drain
# 贝利尔外观（add_belial_model.py）
execute if entity @s[tag=rpg.bll] run function rpg:belial_lord/skill/sk6_3
