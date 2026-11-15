# 被诅咒的人（as/at 他）：暗红符文在头顶，倒数，到时炸开
scoreboard players remove @s rpg_jq_cu 1
execute if score @s rpg_jq_cu matches ..0 run return run function rpg:jacques_boss/curse/pop
particle minecraft:dust{color:[0.55,0.04,0.08],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 2
scoreboard players operation #m rpg_jq = @s rpg_jq_cu
scoreboard players set #k rpg_jq 8
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.90 ~0.15 ~0.00 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 0 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.45 ~0.15 ~0.78 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 0 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.45 ~0.15 ~-0.78 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 1 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.64 ~0.15 ~0.64 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 1 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.87 ~0.15 ~0.23 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 1 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.23 ~0.15 ~-0.87 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 2 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.00 ~0.15 ~0.90 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 2 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.78 ~0.15 ~-0.45 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 2 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.78 ~0.15 ~-0.45 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 3 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.64 ~0.15 ~0.64 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 3 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.23 ~0.15 ~-0.87 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 3 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.87 ~0.15 ~0.23 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 4 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.90 ~0.15 ~0.00 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 4 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.45 ~0.15 ~-0.78 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 4 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.45 ~0.15 ~0.78 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 5 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.64 ~0.15 ~-0.64 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 5 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.87 ~0.15 ~-0.23 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 5 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.23 ~0.15 ~0.87 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 6 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.00 ~0.15 ~-0.90 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 6 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.78 ~0.15 ~0.45 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 6 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.78 ~0.15 ~0.45 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 7 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.64 ~0.15 ~-0.64 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 7 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~0.23 ~0.15 ~0.87 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 7 run particle minecraft:dust{color:[0.6,0.03,0.08],scale:1.6} ~-0.87 ~0.15 ~-0.23 0 0.02 0 0.01 1
scoreboard players operation #m rpg_jq = @s rpg_jq_cu
scoreboard players set #k rpg_jq 20
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run function rpg:jacques_boss/curse/beat
