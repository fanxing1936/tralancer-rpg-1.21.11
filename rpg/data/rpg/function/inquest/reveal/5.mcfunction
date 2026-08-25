tag @s add rpg.name.5
scoreboard players set @s rpg_case5 3
title @s times 10 70 20
title @s title ["",{"text":"真　名　确　证","color":"#FFF2A8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"弱点 · 暴怒会被不还手的寒意冷却","color":"#7B241C","bold":true,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"萨麦尔","color":"#7B241C","bold":true,"italic":false},{"text":"　弱点媒介：","color":"gray","italic":false},{"text":"雪球 · 熄怒之雪","color":"white","bold":true,"italic":false},{"text":"。","color":"gray","italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page5
