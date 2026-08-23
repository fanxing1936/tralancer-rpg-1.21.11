# 走完了。有东西从这个人身上挣了出来。
tag @s remove rpg.taint.full
scoreboard players set @s rpg_fall 0
attribute @s minecraft:attack_damage modifier remove rpg:fall

# 掏空之后并不干净 —— 还剩这么多，下一轮从这里重新爬。
scoreboard players set @s rpg_taint 40
scoreboard players set @s rpg_taint_t 0

title @s times 10 80 30
title @s title ["",{"text":"降　临","italic":false,"color":"dark_red","bold":true}]
title @s subtitle ["",{"text":"它不再需要借你的手了","italic":false,"color":"gray","italic":true}]
effect give @s minecraft:weakness 12 1 true
effect give @s minecraft:slowness 12 1 true
effect give @s minecraft:nausea 10 0 true
effect give @s minecraft:blindness 3 0 true
damage @s 8 minecraft:magic

# 认主：签了哪一柱，挣出来的就是哪一位。没签的话是个无名的东西。
scoreboard players set #lord rpg_fall 0
execute if entity @s[tag=rpg.pact] run scoreboard players operation #lord rpg_fall = @s rpg_pact
execute at @s run function rpg:taint/advent_at
