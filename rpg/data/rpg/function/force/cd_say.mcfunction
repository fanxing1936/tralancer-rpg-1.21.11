# #s = 剩余秒数
execute if score @s rpg_fo_msg > #now rpg_fo run return 0
scoreboard players operation @s rpg_fo_msg = #now rpg_fo
scoreboard players add @s rpg_fo_msg 10
playsound minecraft:block.dispenser.fail player @s ~ ~ ~ 0.6 1.4
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"还在冷却：","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"#s","objective":"rpg_fo"},"color":"#E6DFCF"},{"text":" 秒","color":"#9C9A94","bold":false,"italic":false}]
