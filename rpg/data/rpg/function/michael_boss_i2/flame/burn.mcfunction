# 余烬（as/at 玩家）：3 秒，每秒 1
scoreboard players remove @s rpg_mk_r 1
scoreboard players operation #m rpg_mk_i2 = @s rpg_mk_r
scoreboard players set #k rpg_mk_i2 20
scoreboard players operation #m rpg_mk_i2 %= #k rpg_mk_i2
execute if score #m rpg_mk_i2 matches 0 run damage @s 1 minecraft:on_fire
particle minecraft:flame ~ ~0.8 ~ 0.3 0.5 0.3 0.01 2
