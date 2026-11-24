scoreboard players set @s rpg_daath 1
scoreboard players add @s rpg_ex_xp 100
scoreboard players add @s rpg_sp 1
title @s times 10 60 20
title @s subtitle {"text":"Daath · דעת","color":"#AAB4C3","bold":false,"italic":true}
title @s title ["",{"text":"越过深渊","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.5 1.4
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"达阿特已越过：阅历 +100、技能点 +1。","color":"#E6DFCF","bold":false,"italic":false}]
