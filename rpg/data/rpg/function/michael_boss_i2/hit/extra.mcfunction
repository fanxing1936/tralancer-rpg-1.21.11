# 显形中：这一下再多扣一半（as 他）
execute store result score #h rpg_mk_i2 run data get entity @s Health 10
scoreboard players operation #dd rpg_mk_i2 /= #two rpg_mk_i2
scoreboard players operation #h rpg_mk_i2 -= #dd rpg_mk_i2
execute if score #h rpg_mk_i2 matches ..10 run scoreboard players set #h rpg_mk_i2 10
execute store result entity @s Health float 0.1 run scoreboard players get #h rpg_mk_i2
execute at @s run particle minecraft:damage_indicator ~ ~1.4 ~ 0.3 0.3 0.3 0.2 6
