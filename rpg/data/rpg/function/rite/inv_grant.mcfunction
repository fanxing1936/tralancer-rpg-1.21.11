# 圣痕落定。增益一次性按整段时长给足，之后每刻只剩计时和光晕。
tag @s remove rpg.inv.subject
scoreboard players set @s rpg_inv 0
tag @s remove rpg.taint.full
scoreboard players set @s rpg_taint 0
# 反转烧掉的是污染的一切 —— 柱位也在其中。这是唯一的解约途径。
execute if entity @s[tag=rpg.pact] run function rpg:pact/break
scoreboard players set @s rpg_holy 3600
effect give @s minecraft:instant_health 1 2 true
effect give @s minecraft:strength 180 1 true
effect give @s minecraft:resistance 180 0 true
effect give @s minecraft:regeneration 180 0 true
effect give @s minecraft:fire_resistance 180 0 true
effect give @s minecraft:absorption 180 1 true
title @s times 10 70 20
title @s title ["",{"text":"圣 痕","italic":false,"color":"gold","bold":true}]
title @s subtitle ["",{"text":"负与负相乘，污染发生反转","italic":false,"color":"yellow"}]
