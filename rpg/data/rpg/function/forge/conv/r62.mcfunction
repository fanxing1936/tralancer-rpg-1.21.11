# 换下界合金锭
execute store result score #c rpg_fg run clear @s minecraft:diamond[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 16.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　钻石不够（要 16）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute unless score #c rpg_fg matches 8.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　残魂不够（要 8）","color":"#C04A3C","bold":false,"italic":false}]
clear @s minecraft:diamond[!minecraft:custom_data] 16
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 8
function rpg:quest/hook/conv
loot give @s loot rpg:world/raw/netherite_ingot
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 0.8 1.2
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　换得 ","color":"#9C9A94","bold":false,"italic":false},{"text":"下界合金锭 ×1","color":"#E6DFCF","bold":true,"italic":false}]
function rpg:forge/conv/open
