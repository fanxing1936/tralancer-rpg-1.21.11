# 灵体常驻（as/at 他）：身边慢慢上飘的白色灵光；二阶段六翼边缘飘火星
scoreboard players operation #m rpg_mk_i1 = #tick rpg_mk_i1
scoreboard players set #k rpg_mk_i1 5
scoreboard players operation #m rpg_mk_i1 %= #k rpg_mk_i1
execute if score #m rpg_mk_i1 matches 0 run particle minecraft:end_rod ~ ~1.2 ~ 0.5 0.8 0.5 0.01 1
execute if score #m rpg_mk_i1 matches 2 run particle minecraft:white_ash ~ ~1.4 ~ 0.6 0.8 0.6 0 3
execute if score @s rpg_mk_i1 matches 2 if score #m rpg_mk_i1 matches 1 run particle minecraft:flame ^ ^1.6 ^-0.6 0.9 0.5 0.2 0.01 2
execute if score @s rpg_mk_i1 matches 2 if score #m rpg_mk_i1 matches 3 run particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ^ ^1.4 ^-0.5 0.8 0.6 0.2 0 2
