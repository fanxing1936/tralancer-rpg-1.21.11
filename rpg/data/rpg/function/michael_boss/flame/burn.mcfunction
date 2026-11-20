# 余烬（as/at 玩家）：3 秒，每秒 1
scoreboard players remove @s rpg_mk_r 1
scoreboard players operation #m rpg_mk = @s rpg_mk_r
scoreboard players set #k rpg_mk 20
scoreboard players operation #m rpg_mk %= #k rpg_mk
execute if score #m rpg_mk matches 0 run damage @s 1 minecraft:on_fire
particle minecraft:flame ~ ~0.8 ~ 0.3 0.5 0.3 0.01 2
