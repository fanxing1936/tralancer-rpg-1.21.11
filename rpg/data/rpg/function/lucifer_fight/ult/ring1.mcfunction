tag @e[tag=rpg.unit] remove rpg.lu2f.hit
tag @s add rpg.dm.cast
execute as @e[type=minecraft:marker,tag=rpg.lu2f.r1] if score @s rpg_l2_id = #id rpg_l2_id at @s run function rpg:lucifer_fight/ult/erupt
tag @s remove rpg.dm.cast
tag @e[tag=rpg.unit] remove rpg.lu2f.hit
playsound rpg:lucifer_p2.vine_burst_new hostile @a[distance=..40] ~ ~ ~ 1.3 1
