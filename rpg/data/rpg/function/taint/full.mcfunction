# 魔化到顶。这里**不给出路** —— 逆圣化还在，但不再有人告诉你它存在。
tag @s add rpg.taint.full
scoreboard players set @s rpg_fall 0
title @s times 10 70 25
title @s title ["",{"text":"堕 落 开 始","italic":false,"color":"dark_red","bold":true}]
title @s subtitle ["",{"text":"你手上的力量正在变大 —— 那不是你的","italic":false,"color":"dark_gray","italic":true}]
playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.6 1.6
playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1 0.5
execute at @s run particle sculk_charge_pop ~ ~1.2 ~ 0.4 0.6 0.4 0.05 30
