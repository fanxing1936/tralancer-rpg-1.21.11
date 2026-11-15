execute at @s as @e[tag=rpg.unit.f,distance=..18] run function rpg:hud/demon/m43
particle dust{color:[0.90,0.64,0.24],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
# 玛门外观（add_mammon_model.py）
execute if entity @s[tag=rpg.mml] run function rpg:mammon_lord/skill/ult7_warn
