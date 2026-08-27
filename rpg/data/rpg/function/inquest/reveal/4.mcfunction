tag @s add rpg.name.4
execute unless entity @s[tag=rpg.endless.invited] run function rpg:entry/endless/invite
scoreboard players set @s rpg_case4 3
title @s times 15 55 20
title @s title ["",{"text":"真名确证","color":"#62D9E8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"别西卜 · 暴食","color":"#5A6B1E","bold":false,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#62D9E8","bold":true,"italic":false},{"text":"别西卜 · 暴食","color":"#5A6B1E","bold":false,"italic":false},{"text":"　弱点：","color":"gray","bold":false,"italic":false},{"text":"腐败的宴席","color":"#FFF2A8","bold":false,"italic":false}]
tellraw @s ["",{"text":"◆ ","color":"#62D9E8","bold":false,"italic":false},{"text":"暴食无法吞下已经腐败的宴席。","color":"gray","bold":false,"italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page4
