tag @s add rpg.name.7
execute unless entity @s[tag=rpg.endless.invited] run function rpg:entry/endless/invite
scoreboard players set @s rpg_case7 3
title @s times 10 70 20
title @s title ["",{"text":"真　名　确　证","color":"#FFF2A8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"弱点 · 贪婪无法夺走主动舍弃之物","color":"#B7950B","bold":true,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"玛门","color":"#B7950B","bold":false,"italic":false},{"text":"　弱点媒介：","color":"gray","italic":false},{"text":"金锭 · 自愿之金","color":"white","bold":true,"italic":false},{"text":"。","color":"gray","italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page7
