scoreboard players set #sk rpg_pf 1
scoreboard players set #st rpg_pf 0
scoreboard players set #walking rpg_pf 0
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] at @s run function rpg:heart_of_ender/anim/enter/rise
