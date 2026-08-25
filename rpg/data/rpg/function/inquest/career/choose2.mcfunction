execute unless score @s rpg_ex_path matches 0 run return 0
scoreboard players set @s rpg_ex_path 2
tellraw @s ["",{"text":"[路线确立] ","color":"#8FC7FF","bold":true,"italic":false},{"text":"守护。此选择不可随意撤销。","color":"gray","italic":false}]
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1.2
function rpg:inquest/career/claim
