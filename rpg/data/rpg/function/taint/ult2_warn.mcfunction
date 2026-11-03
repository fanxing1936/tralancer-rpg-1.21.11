execute at @s as @a[distance=..18,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m38
particle dust{color:[0.31,0.62,0.94],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
# 利维坦外观（add_leviathan_model.py）
execute if entity @s[tag=rpg.lv] run function rpg:leviathan/skill/ult2_warn
