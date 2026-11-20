# 把这一下整下退回（as 他）
execute store result score #h rpg_sl run data get entity @s Health 10
scoreboard players operation #h rpg_sl += #dd rpg_sl
execute if score #h rpg_sl matches 10000.. run scoreboard players set #h rpg_sl 10000
execute store result entity @s Health float 0.1 run scoreboard players get #h rpg_sl
