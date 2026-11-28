execute if entity @s[tag=rpg.dm] run return 0
tellraw @s ["",{"text":"〖","color":"#A276BE","bold":true,"italic":false},{"text":"罪仆","color":"#A276BE","bold":true,"italic":false},{"text":"〗","color":"#A276BE","bold":true,"italic":false},{"text":" 𝔖𝔦𝔫-𝔰𝔢𝔯𝔳𝔞𝔫𝔱","color":"#8F7430","italic":false},{"text":"  契成。欢迎回家。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"It is done. Welcome home.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.sv05 voice @s ~ ~ ~ 1 1
tag @s add rpg.dm
team join rpg_dm @s
scoreboard players add @s rpg_taint 30
scoreboard players add @s rpg_dm_rep 10
title @s times 10 60 20
title @s title ["",{"text":"投诚","color":"#A276BE","bold":true,"italic":false}]
title @s subtitle ["",{"text":"你的名字前多了一枚魔印","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:entity.wither.spawn hostile @s ~ ~ ~ 0.5 1.4
