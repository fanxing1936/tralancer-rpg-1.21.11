execute if entity @s[tag=rpg.t.meteor] run return 0
tag @s add rpg.t.meteor
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.4
tellraw @s ["",{"text":"[称号]","color":"#FFD85A","bold":true,"italic":false},{"text":"　","color":"gray","bold":false,"italic":false},{"text":"","font":"rpg:world_titles","color":"white"},{"text":" 白昼流星","color":"#FFFFFF","bold":true,"italic":false},{"text":"　王冠阶的正午，对着太阳举起无垠星空。在「旅程」页的称号里戴上它。","color":"gray","bold":false,"italic":false}]
