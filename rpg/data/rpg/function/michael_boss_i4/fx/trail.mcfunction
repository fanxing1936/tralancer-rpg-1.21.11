# 火路（as/at 标记）：每 10 刻烧一下站在上面的人
scoreboard players operation #m rpg_mk_i4 = @s rpg_mk_life
scoreboard players set #k rpg_mk_i4 3
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 run particle minecraft:flame ~ ~0.2 ~ 0.3 0.05 0.3 0.01 2
execute if score @s rpg_mk_life matches 50 run function rpg:michael_boss_i4/trail/burn
execute if score @s rpg_mk_life matches 30 run function rpg:michael_boss_i4/trail/burn
execute if score @s rpg_mk_life matches 10 run function rpg:michael_boss_i4/trail/burn
