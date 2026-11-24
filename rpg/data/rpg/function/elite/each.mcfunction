# 每只精英每秒（as/at）
execute if score @s rpg_el_a1 matches 1 run particle minecraft:dust{color:[0.38,0.85,0.91],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 1 run particle minecraft:dust{color:[0.38,0.85,0.91],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 2 run particle minecraft:dust{color:[0.82,0.82,0.82],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 2 run particle minecraft:dust{color:[0.82,0.82,0.82],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 3 run particle minecraft:dust{color:[1.00,0.42,0.37],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 3 run particle minecraft:dust{color:[1.00,0.42,0.37],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 4 run particle minecraft:dust{color:[0.85,0.48,0.85],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 4 run particle minecraft:dust{color:[0.85,0.48,0.85],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 5 run particle minecraft:dust{color:[0.91,0.96,1.00],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 5 run particle minecraft:dust{color:[0.91,0.96,1.00],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 6 run particle minecraft:dust{color:[0.44,0.86,0.44],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 6 run particle minecraft:dust{color:[0.44,0.86,0.44],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 7 run particle minecraft:dust{color:[1.00,0.64,0.36],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 7 run particle minecraft:dust{color:[1.00,0.64,0.36],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 8 run particle minecraft:dust{color:[0.64,0.46,0.75],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 8 run particle minecraft:dust{color:[0.64,0.46,0.75],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 9 run particle minecraft:dust{color:[0.78,0.45,0.60],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 9 run particle minecraft:dust{color:[0.78,0.45,0.60],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if score @s rpg_el_a1 matches 10 run particle minecraft:dust{color:[1.00,0.85,0.35],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 4
execute if score @s rpg_el_a2 matches 10 run particle minecraft:dust{color:[1.00,0.85,0.35],scale:1.0} ~ ~1.4 ~ 0.4 0.6 0.4 0 3
execute if entity @s[scores={rpg_el_a1=3}] run function rpg:elite/a/3/sec
execute if entity @s[scores={rpg_el_a2=3}] run function rpg:elite/a/3/sec
execute if entity @s[scores={rpg_el_a1=8}] run function rpg:elite/a/8/sec
execute if entity @s[scores={rpg_el_a2=8}] run function rpg:elite/a/8/sec
execute if entity @s[tag=rpg.el.boss] if entity @a[distance=..24] run function rpg:elite/bar
