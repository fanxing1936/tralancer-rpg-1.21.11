# 「最后一课」被躲开、他跪地时：这一下再多扣一半（as 他）
execute store result score #h rpg_sl run data get entity @s Health 10
scoreboard players operation #dd rpg_sl /= #two rpg_sl
scoreboard players operation #h rpg_sl -= #dd rpg_sl
execute if score #h rpg_sl matches ..10 run scoreboard players set #h rpg_sl 10
execute store result entity @s Health float 0.1 run scoreboard players get #h rpg_sl
particle minecraft:damage_indicator ~ ~1.4 ~ 0.3 0.3 0.3 0.2 6
