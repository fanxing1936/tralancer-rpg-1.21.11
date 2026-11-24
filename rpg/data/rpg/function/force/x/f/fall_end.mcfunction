scoreboard players set @s rpg_fo_fl 0
scoreboard players add @s rpg_taint 20
playsound minecraft:entity.wither.ambient player @s ~ ~ ~ 0.6 0.8
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"堕天结束 · 魔化 +20","color":"#A276BE","bold":false,"italic":false}]
