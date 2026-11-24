# 晋入第 1 阶 · 王国
scoreboard players set @s rpg_sef 1
scoreboard players add @s rpg_sp 1
function rpg:sephira/bonus/apply
title @s times 10 60 20
title @s subtitle {"text":"Malkuth · מלכות","color":"#C58A62","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"王国","color":"#C58A62","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 0.76
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 1 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"王国","color":"#C58A62","bold":true,"italic":false},{"text":"　技能点 +1","color":"#E6DFCF","bold":false,"italic":false}]
