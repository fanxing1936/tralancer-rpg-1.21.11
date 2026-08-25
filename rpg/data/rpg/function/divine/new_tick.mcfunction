execute if score @s rpg_lt_auth matches ..-1 run scoreboard players set @s rpg_lt_auth 0
execute if score @s rpg_lt_auth matches 101.. run scoreboard players set @s rpg_lt_auth 100
execute if score @s rpg_lt_auth matches ..99 run scoreboard players add @s rpg_lt_auth_t 1
execute if score @s rpg_lt_auth_t matches 40.. if score @s rpg_lt_auth matches ..99 run scoreboard players add @s rpg_lt_auth 1
execute if score @s rpg_lt_auth_t matches 40.. run scoreboard players set @s rpg_lt_auth_t 0
execute if score @s rpg_lt_auth matches 100.. run scoreboard players set @s rpg_lt_auth_t 0
execute if score @s rpg_lt_judge matches 1.. run scoreboard players remove @s rpg_lt_judge 1
scoreboard players set @s rpg_taint 0
tag @s remove rpg.taint.full
effect clear @s minecraft:blindness
effect clear @s minecraft:darkness
