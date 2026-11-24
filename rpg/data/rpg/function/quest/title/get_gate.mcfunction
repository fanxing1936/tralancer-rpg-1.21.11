execute if entity @s[tag=rpg.t.gate] run return 0
tag @s add rpg.t.gate
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.4
tellraw @s ["",{"text":"[称号]","color":"#FFD85A","bold":true,"italic":false},{"text":"　","color":"gray","bold":false,"italic":false},{"text":"","font":"rpg:world_titles","color":"white"},{"text":" 所罗门的门户","color":"#FFFFFF","bold":true,"italic":false},{"text":"　左手雅斤，右手波阿斯，在高处站了十秒。在「旅程」页的称号里戴上它。","color":"gray","bold":false,"italic":false}]
