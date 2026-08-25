tag @s add rpg.name.3
scoreboard players set @s rpg_case3 3
title @s times 10 70 20
title @s title ["",{"text":"真　名　确　证","color":"#FFF2A8","bold":true,"italic":false}]
title @s subtitle ["",{"text":"弱点 · 怠惰畏惧持续前行的时间","color":"#6A6A70","bold":true,"italic":false}]
tellraw @s ["",{"text":"[真名确证] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"亚巴顿","color":"#6A6A70","bold":true,"italic":false},{"text":"　弱点媒介：","color":"gray","italic":false},{"text":"时钟 · 不眠之钟","color":"white","bold":true,"italic":false},{"text":"。","color":"gray","italic":false}]
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.35
scoreboard players add @s rpg_ex_xp 8
function rpg:inquest/give/page3
