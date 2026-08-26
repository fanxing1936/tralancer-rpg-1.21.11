tag @s add rpg.name.6
scoreboard players set @s rpg_case6 3
title @s times 10 70 20
title @s title ["",{"text":"真　名　确　证","color":"#FFF2A8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"弱点 · 色欲惧怕不被幻象改写的映照","color":"#5B2C6F","bold":true,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"贝利尔","color":"#5B2C6F","bold":false,"italic":false},{"text":"　弱点媒介：","color":"gray","italic":false},{"text":"紫水晶碎片 · 清醒之镜","color":"white","bold":true,"italic":false},{"text":"。","color":"gray","italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page6
