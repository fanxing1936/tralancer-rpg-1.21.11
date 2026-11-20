scoreboard players set @s rpg_sl_sk 0
scoreboard players set @s rpg_sl_busy 0
tag @s remove rpg.slb.guard
tag @s remove rpg.slb.weak
tag @s remove rpg.slb.hidden
data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}
execute if score @s rpg_sl matches 1 run attribute @s minecraft:armor base set 14
execute if score @s rpg_sl matches 2 run attribute @s minecraft:armor base set 6
execute as @e[type=minecraft:vindicator,tag=rpg.slg] run function rpg:saul_boss/clear_unit
