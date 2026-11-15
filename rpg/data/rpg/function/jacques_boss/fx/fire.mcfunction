# 地上的火（as/at 标记）：粒子；每 10 刻烧一次站在里面的人
scoreboard players operation #m rpg_jq = @s rpg_jq_life
scoreboard players set #k rpg_jq 4
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run particle minecraft:flame ~ ~0.2 ~ 0.4 0.1 0.4 0.01 4
execute if score #m rpg_jq matches 2 run particle minecraft:small_flame ~ ~0.5 ~ 0.3 0.3 0.3 0.01 2
execute if score #m rpg_jq matches 1 run particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ~ ~0.4 ~ 0.35 0.2 0.35 0 1
scoreboard players operation #m rpg_jq = @s rpg_jq_life
scoreboard players set #k rpg_jq 10
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 as @e[tag=rpg.unit.f,distance=..1.1] run damage @s 2 minecraft:in_fire
scoreboard players operation #m rpg_jq = @s rpg_jq_life
scoreboard players set #k rpg_jq 16
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run particle minecraft:lava ~ ~0.2 ~ 0.3 0 0.3 0 1
