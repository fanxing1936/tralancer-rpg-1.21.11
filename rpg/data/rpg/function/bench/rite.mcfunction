execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank_rite"}] run return run function rpg:alc/open_rite
execute if items entity @s weapon.mainhand * run return run tellraw @s ["",{"text":"[工作台] ","color":"#E39745","bold":true,"italic":false},{"text":"先空出主手，或主手拿着空白圣具","color":"#FF6B5E","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s *[minecraft:custom_data~{rpg_mat:"blank_rite"}] 0
execute if score #c rpg_fg matches 0 run return run tellraw @s ["",{"text":"[工作台] ","color":"#E39745","bold":true,"italic":false},{"text":"身上没有空白圣具","color":"#FF6B5E","bold":false,"italic":false}]
clear @s *[minecraft:custom_data~{rpg_mat:"blank_rite"}] 1
loot replace entity @s weapon.mainhand loot rpg:potion/blank_rite
function rpg:alc/open_rite
