execute if entity @s[tag=rpg.t.bard] run return 0
tag @s add rpg.t.bard
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.4
tellraw @s ["",{"text":"[称号]","color":"#FFD85A","bold":true,"italic":false},{"text":"　","color":"gray","bold":false,"italic":false},{"text":"","font":"rpg:world_titles","color":"white"},{"text":" 三首歌的听者","color":"#FFFFFF","bold":true,"italic":false},{"text":"　替吟游诗人拣齐了三首歌。在「旅程」页的称号里戴上它。","color":"gray","bold":false,"italic":false}]
