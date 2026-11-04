execute at @s as @a[distance=..18,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m39
particle dust{color:[0.65,0.69,0.79],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
# 亚巴顿外观（add_abaddon_model.py）
execute if entity @s[tag=rpg.ab] run function rpg:abaddon/skill/ult3_warn
