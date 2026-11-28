scoreboard players set @s rpg_mk_sk 0
scoreboard players set @s rpg_mk_busy 0
tag @s remove rpg.mkb.fold
tag @s remove rpg.mkb.air
data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}
execute if score @s rpg_mk_i4 matches 1 run attribute @s minecraft:armor base set 12
execute if score @s rpg_mk_i4 matches 2 run attribute @s minecraft:armor base set 8
