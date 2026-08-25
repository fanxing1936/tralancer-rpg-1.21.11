execute unless score @s rpg_ex_path matches 0 run return 0
scoreboard players set @s rpg_ex_path 1
tellraw @s ["",{"text":"[路线确立] ","color":"#FF806B","bold":true,"italic":false},{"text":"审判。此选择不可随意撤销。","color":"gray","italic":false}]
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1.2
function rpg:inquest/career/claim
