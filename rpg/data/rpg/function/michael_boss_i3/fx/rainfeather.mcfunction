execute if score @s rpg_mk_life matches 14 run data merge entity @s {teleport_duration:12}
execute if score @s rpg_mk_life matches 14 run tp @s ~ ~-8.4 ~
execute if score @s rpg_mk_life matches 3..13 run particle minecraft:flame ~ ~0.3 ~ 0.05 0.2 0.05 0.01 1
