# 退回这一下的 #f 成（as 他）
scoreboard players operation #dd rpg_mk_i4 *= #f rpg_mk_i4
scoreboard players operation #dd rpg_mk_i4 /= #ten rpg_mk_i4
execute store result score #h rpg_mk_i4 run data get entity @s Health 10
scoreboard players operation #h rpg_mk_i4 += #dd rpg_mk_i4
execute if score #h rpg_mk_i4 matches 12000.. run scoreboard players set #h rpg_mk_i4 12000
execute store result entity @s Health float 0.1 run scoreboard players get #h rpg_mk_i4
