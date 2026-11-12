tag @s add rpg.dm.cast
execute as @e[type=minecraft:marker,tag=rpg.lu2f.vmark] if score @s rpg_l2_id = #id rpg_l2_id at @s run function rpg:lucifer_fight/vine/erupt
tag @s remove rpg.dm.cast
playsound rpg:lucifer_p2.vine_burst_new hostile @a[distance=..32] ~ ~ ~ 1.2 1
scoreboard players operation @s rpg_l2_v = #hit rpg_l2_v
tag @a remove rpg.lu2f.hit
