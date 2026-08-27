tag @s add rpg.name.1
execute unless entity @s[tag=rpg.endless.invited] run function rpg:entry/endless/invite
scoreboard players set @s rpg_case1 3
title @s times 10 70 20
title @s title ["",{"text":"真　名　确　证","color":"#FFF2A8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"弱点 · 傲慢无法承受自愿的低伏","color":"#00491C","bold":true,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"路西法","color":"#00491C","bold":false,"italic":false},{"text":"　弱点媒介：","color":"gray","italic":false},{"text":"羽毛 · 谦卑之羽","color":"white","bold":true,"italic":false},{"text":"。","color":"gray","italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page1
