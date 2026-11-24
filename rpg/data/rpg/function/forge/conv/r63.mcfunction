# 换金锭
execute store result score #c rpg_fg run clear @s minecraft:gold_nugget[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 9.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　金粒不够（要 9）","color":"#C04A3C","bold":false,"italic":false}]
clear @s minecraft:gold_nugget[!minecraft:custom_data] 9
function rpg:quest/hook/conv
loot give @s loot rpg:world/raw/gold_ingot
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 0.8 1.2
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　换得 ","color":"#9C9A94","bold":false,"italic":false},{"text":"金锭 ×1","color":"#E6DFCF","bold":true,"italic":false}]
function rpg:forge/conv/open
