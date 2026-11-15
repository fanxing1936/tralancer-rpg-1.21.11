# 火圈（as/at 圆心）：环上的粒子；每 10 刻烧一次站在 3～4.5 格环上的人
scoreboard players operation #m rpg_jq = @s rpg_jq_life
scoreboard players set #k rpg_jq 3
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run function rpg:jacques_boss/vfx/firering
scoreboard players operation #m rpg_jq = @s rpg_jq_life
scoreboard players set #k rpg_jq 10
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 as @e[tag=rpg.unit.f,distance=3..4.6] run damage @s 2 minecraft:in_fire
