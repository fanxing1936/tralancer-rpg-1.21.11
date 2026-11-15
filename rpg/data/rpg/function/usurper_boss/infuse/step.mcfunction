scoreboard players add #d rpg_ub 1
execute if entity @s[distance=..1.2] run return 0
execute positioned ~ ~-1.4 ~ if entity @s[distance=..1.2] run return 0
execute if score #d rpg_ub matches ..24 positioned ^ ^ ^1 run function rpg:usurper_boss/infuse/step
