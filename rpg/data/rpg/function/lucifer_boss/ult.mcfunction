execute if score #ult rpg_lub matches 1 run tag @s add rpg.lub.u1
execute if score #ult rpg_lub matches 2 run tag @s add rpg.lub.u2
scoreboard players set @s rpg_lub_c 0
scoreboard players set @s rpg_dm_cd 70
execute if entity @s[tag=rpg.lu.phase2] run function rpg:lucifer_fight/ult/warn
execute unless entity @s[tag=rpg.lu.phase2] run function rpg:lucifer_fight/p1/ult/warn
