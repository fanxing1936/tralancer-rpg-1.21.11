# 它没有普攻动作：迫击动作从张嘴前一点切入，再切回待机，看起来就是一口咬合。
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] at @s run function rpg:heart_of_ender/anim/enter/mortar
scoreboard players set @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] rpg_he_t 20
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] at @s run function rpg:heart_of_ender/anim/mortar/f20
scoreboard players set @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] rpg_he_run 0
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers run data merge entity @s {interpolation_duration:4}
scoreboard players set #bl rpg_pf 4
