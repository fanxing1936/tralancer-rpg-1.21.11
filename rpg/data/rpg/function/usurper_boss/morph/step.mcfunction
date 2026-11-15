scoreboard players add #d rpg_ub 1
execute if entity @e[type=minecraft:vindicator,tag=rpg.usb,distance=..1.4] run return 0
execute positioned ~ ~-1.6 ~ if entity @e[type=minecraft:vindicator,tag=rpg.usb,distance=..1.4] run return 0
execute if score #d rpg_ub matches ..48 positioned ^ ^ ^1 run function rpg:usurper_boss/morph/step
