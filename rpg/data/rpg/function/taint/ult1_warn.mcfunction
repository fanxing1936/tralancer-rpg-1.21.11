# 路西法二阶段（add_lucifer_fight.py）
execute if entity @s[tag=rpg.lu.phase2] run return run function rpg:lucifer_fight/ult/warn
return run function rpg:lucifer_fight/p1/ult/warn
execute at @s as @a[distance=..18,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m37
particle dust{color:[0.37,0.84,0.55],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
# Lucifer mesh appearance (add_lucifer_model.py)
execute if entity @s[tag=rpg.lu,tag=!rpg.lu.phase2] run function rpg:lucifer_lord/skill/ult1_warn
