execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] at @s run function rpg:heart_of_ender/anim/enter/cross_beam
scoreboard players set @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] rpg_he_run 0
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers run data merge entity @s {interpolation_duration:6}
scoreboard players set #bl rpg_pf 6
