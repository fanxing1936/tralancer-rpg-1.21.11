# 魔化到顶。这一刻不是死路 —— 是唯一的岔路口。
tag @s add rpg.taint.full
title @s times 10 60 20
title @s title ["",{"text":"魔 化 已 满","italic":false,"color":"dark_red","bold":true}]
title @s subtitle ["",{"text":"立起驱魔图腾，浇上圣水 —— 反转","italic":false,"color":"gold"}]
playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.5 1.8
execute at @s run particle sculk_charge_pop ~ ~1.2 ~ 0.4 0.6 0.4 0.05 30
