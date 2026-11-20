# 退回这一下的 #f 成（as 他）
scoreboard players operation #dd rpg_mk *= #f rpg_mk
scoreboard players operation #dd rpg_mk /= #ten rpg_mk
execute store result score #h rpg_mk run data get entity @s Health 10
scoreboard players operation #h rpg_mk += #dd rpg_mk
execute if score #h rpg_mk matches 12000.. run scoreboard players set #h rpg_mk 12000
execute store result entity @s Health float 0.1 run scoreboard players get #h rpg_mk
