tag @s add rpg.name.4
scoreboard players set @s rpg_case4 3
title @s times 10 70 20
title @s title ["",{"text":"真　名　确　证","color":"#FFF2A8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"弱点 · 暴食无法吞下已经腐败的宴席","color":"#5A6B1E","bold":true,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"别西卜","color":"#5A6B1E","bold":true,"italic":false},{"text":"　弱点媒介：","color":"gray","italic":false},{"text":"毒马铃薯 · 腐宴残食","color":"white","bold":true,"italic":false},{"text":"。","color":"gray","italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page4
