execute unless score @s rpg_force matches 0 run return 0
execute unless score @s rpg_sef matches 5.. run return 0
scoreboard players set @s rpg_force 1
scoreboard players set @s rpg_vital 100
scoreboard players add @s rpg_sp 2
title @s times 10 50 20
title @s title ["",{"text":"觉醒 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣力","color":"#FFD85A","bold":true,"italic":false}]
playsound minecraft:block.respawn_anchor.charge master @s ~ ~ ~ 1 1
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"觉醒为","color":"#9C9A94","bold":false,"italic":false},{"text":"圣力","color":"#FFD85A","bold":true,"italic":false},{"text":" · 技能点 +2","color":"#E6DFCF","bold":false,"italic":false}]
