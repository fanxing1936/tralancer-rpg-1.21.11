execute if score @s rpg_mk_life matches 13 run data merge entity @s {teleport_duration:10}
execute if score @s rpg_mk_life matches 13 run tp @s ~ ~-13.6 ~
execute if score @s rpg_mk_life matches 3..12 run particle minecraft:flame ~ ~0.4 ~ 0.1 0.3 0.1 0.02 2
execute if score @s rpg_mk_life matches 2 run function rpg:michael_boss_i3/stars/land
execute if score @s rpg_mk_life matches 2 run particle minecraft:flame ~ ~0.2 ~ 0.6 0.1 0.6 0.05 10
function rpg:michael_boss_i3/fx/kind
