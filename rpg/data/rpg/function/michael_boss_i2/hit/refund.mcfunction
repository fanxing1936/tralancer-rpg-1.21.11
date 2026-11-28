# 退回这一下的 #f 成（as 他）
scoreboard players operation #dd rpg_mk_i2 *= #f rpg_mk_i2
scoreboard players operation #dd rpg_mk_i2 /= #ten rpg_mk_i2
execute store result score #h rpg_mk_i2 run data get entity @s Health 10
scoreboard players operation #h rpg_mk_i2 += #dd rpg_mk_i2
execute if score #h rpg_mk_i2 matches 12000.. run scoreboard players set #h rpg_mk_i2 12000
execute store result entity @s Health float 0.1 run scoreboard players get #h rpg_mk_i2
