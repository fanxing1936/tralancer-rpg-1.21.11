# 地上的蛛网（as/at 标记）：踩上去缓慢
scoreboard players operation #m rpg_sl = @s rpg_sl_life
scoreboard players set #k rpg_sl 10
scoreboard players operation #m rpg_sl %= #k rpg_sl
execute if score #m rpg_sl matches 0 as @e[tag=rpg.unit.f,distance=..1.4] run effect give @s minecraft:slowness 3 2
execute if score #m rpg_sl matches 5 run particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~ ~0.2 ~ 0.6 0.05 0.6 0 2
