# 二阶段常驻（as/at 他）：身上挂着的蛛丝，红眼一点暗红
scoreboard players operation #m rpg_sl = #tick rpg_sl
scoreboard players set #k rpg_sl 6
scoreboard players operation #m rpg_sl %= #k rpg_sl
execute if score #m rpg_sl matches 0 run particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~ ~1.2 ~ 0.35 0.7 0.35 0 1
execute if score #m rpg_sl matches 3 run particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ^ ^1.72 ^0.2 0.08 0.04 0.08 0 1
