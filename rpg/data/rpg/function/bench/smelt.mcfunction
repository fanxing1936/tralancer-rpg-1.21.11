execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run function rpg:forge/smelt/open
execute if items entity @s weapon.mainhand * run return run tellraw @s ["",{"text":"[工作台] ","color":"#E39745","bold":true,"italic":false},{"text":"先空出主手，或主手拿着器胚","color":"#FF6B5E","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s *[minecraft:custom_data~{rpg_mat:"blank"}] 0
execute if score #c rpg_fg matches 0 run return run tellraw @s ["",{"text":"[工作台] ","color":"#E39745","bold":true,"italic":false},{"text":"身上没有器胚","color":"#FF6B5E","bold":false,"italic":false}]
clear @s *[minecraft:custom_data~{rpg_mat:"blank"}] 1
loot replace entity @s weapon.mainhand loot rpg:forge/item/blank
function rpg:forge/smelt/open
