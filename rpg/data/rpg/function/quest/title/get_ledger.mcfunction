execute if entity @s[tag=rpg.t.ledger] run return 0
tag @s add rpg.t.ledger
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.4
tellraw @s ["",{"text":"[称号]","color":"#FFD85A","bold":true,"italic":false},{"text":"　","color":"gray","bold":false,"italic":false},{"text":"","font":"rpg:world_titles","color":"white"},{"text":" 所罗门的账簿","color":"#FFFFFF","bold":true,"italic":false},{"text":"　七柱三十五名罪仆都亲手打败过。在「旅程」页的称号里戴上它。","color":"gray","bold":false,"italic":false}]
