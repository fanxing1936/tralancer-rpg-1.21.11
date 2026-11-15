scoreboard players operation #m rpg_jq = #tick rpg_jq
scoreboard players set #k rpg_jq 3
scoreboard players operation #m rpg_jq %= #k rpg_jq
# 二阶段：他身上一直在烧（盔甲边缘、坟墓克星）
execute if score #m rpg_jq matches 0 run particle minecraft:flame ~ ~1.2 ~ 0.3 0.6 0.3 0.01 2
execute if score #m rpg_jq matches 1 run particle minecraft:small_flame ~ ~2 ~ 0.3 0.3 0.3 0.01 2
execute if score #m rpg_jq matches 2 run particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ~ ~1.4 ~ 0.35 0.7 0.35 0 2
scoreboard players operation #m rpg_jq = #tick rpg_jq
scoreboard players set #k rpg_jq 10
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run particle minecraft:flame ~0.65 ~0.10 ~0.00 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 0 run particle minecraft:flame ~-0.65 ~0.10 ~0.00 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 1 run particle minecraft:flame ~0.53 ~0.34 ~0.38 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 1 run particle minecraft:flame ~-0.53 ~0.34 ~-0.38 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 2 run particle minecraft:flame ~0.20 ~0.59 ~0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 2 run particle minecraft:flame ~-0.20 ~0.59 ~-0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 3 run particle minecraft:flame ~-0.20 ~0.83 ~0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 3 run particle minecraft:flame ~0.20 ~0.83 ~-0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 4 run particle minecraft:flame ~-0.53 ~1.08 ~0.38 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 4 run particle minecraft:flame ~0.53 ~1.08 ~-0.38 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 5 run particle minecraft:flame ~-0.65 ~1.32 ~0.00 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 5 run particle minecraft:flame ~0.65 ~1.32 ~-0.00 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 6 run particle minecraft:flame ~-0.53 ~1.57 ~-0.38 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 6 run particle minecraft:flame ~0.53 ~1.57 ~0.38 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 7 run particle minecraft:flame ~-0.20 ~1.81 ~-0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 7 run particle minecraft:flame ~0.20 ~1.81 ~0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 8 run particle minecraft:flame ~0.20 ~2.06 ~-0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 8 run particle minecraft:flame ~-0.20 ~2.06 ~0.62 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 9 run particle minecraft:flame ~0.53 ~2.30 ~-0.38 0 0.02 0 0.01 1
execute if score #m rpg_jq matches 9 run particle minecraft:flame ~-0.53 ~2.30 ~0.38 0 0.02 0 0.01 1
scoreboard players operation #m rpg_jq = #tick rpg_jq
scoreboard players set #k rpg_jq 14
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 1
execute if score #m rpg_jq matches 7 run particle minecraft:large_smoke ~ ~2.3 ~ 0.2 0.1 0.2 0.01 1
