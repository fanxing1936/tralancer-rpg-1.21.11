execute store result score #n rpg_fg run clear @s *[minecraft:custom_data~{ebb_tag:1b,add_weapon_tag:1b}]
execute store result storage rpg:forge cv.n int 1 run scoreboard players get #n rpg_fg
function rpg:forge/conv/give_rune_swift with storage rpg:forge cv
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　旧材料换成了新的养成材料","color":"#AAAAAA","italic":false}]
