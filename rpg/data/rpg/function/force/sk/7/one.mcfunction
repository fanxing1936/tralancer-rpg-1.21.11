effect clear @s minecraft:poison
effect clear @s minecraft:wither
effect clear @s minecraft:slowness
effect clear @s minecraft:weakness
effect clear @s minecraft:blindness
effect clear @s minecraft:nausea
effect clear @s minecraft:hunger
effect clear @s minecraft:mining_fatigue
effect clear @s minecraft:darkness
effect clear @s minecraft:levitation
effect clear @s minecraft:unluck
effect clear @s minecraft:infested
effect clear @s minecraft:oozing
effect clear @s minecraft:weaving
effect clear @s minecraft:wind_charged
execute if score #lv rpg_fo matches 1 run scoreboard players remove @s rpg_taint 5
execute if score #lv rpg_fo matches 2 run scoreboard players remove @s rpg_taint 10
execute if score #lv rpg_fo matches 3 run scoreboard players remove @s rpg_taint 15
execute if score @s rpg_taint matches ..-1 run scoreboard players set @s rpg_taint 0
particle minecraft:wax_on ~ ~0.15 ~ 0.4 0.05 0.4 0 6
