execute at @s as @e[tag=rpg.unit.f,distance=..18] run function rpg:hud/demon/m42
particle dust{color:[0.85,0.48,0.85],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
# 贝利尔外观（add_belial_model.py）
execute if entity @s[tag=rpg.bll] run function rpg:belial_lord/skill/ult6_warn
