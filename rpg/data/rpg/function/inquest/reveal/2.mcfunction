tag @s add rpg.name.2
scoreboard players set @s rpg_case2 3
title @s times 10 70 20
title @s title ["",{"text":"真　名　确　证","color":"#FFF2A8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"弱点 · 嫉妒惧怕不属于任何人的馈赠","color":"#1B4F72","bold":true,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"利维坦","color":"#1B4F72","bold":false,"italic":false},{"text":"　弱点媒介：","color":"gray","italic":false},{"text":"海晶砂 · 无主之潮","color":"white","bold":true,"italic":false},{"text":"。","color":"gray","italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page2
