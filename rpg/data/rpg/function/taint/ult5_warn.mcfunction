execute at @s as @e[tag=rpg.unit.f,distance=..18] run function rpg:hud/demon/m41
particle dust{color:[1.00,0.36,0.32],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
# 萨麦尔外观（add_samael_model.py）
execute if entity @s[tag=rpg.sml] run function rpg:samael_lord/skill/ult5_warn
