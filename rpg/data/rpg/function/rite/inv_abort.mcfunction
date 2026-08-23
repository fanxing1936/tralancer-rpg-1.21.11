# 反噬。没熬住的人，得把没烧完的那部分自己吞下去。
tag @s remove rpg.inv.subject
scoreboard players set @s rpg_inv 0
effect give @s minecraft:wither 5 0
effect give @s minecraft:blindness 3 0
playsound minecraft:entity.wither.hurt master @s ~ ~ ~ 1 0.6
title @s times 10 50 20
title @s title ["",{"text":"反 转 失 败","italic":false,"color":"dark_red","bold":true}]
title @s subtitle ["",{"text":"污染未曾松手","italic":false,"color":"gray"}]
