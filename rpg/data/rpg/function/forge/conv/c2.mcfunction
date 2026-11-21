execute store result score #n rpg_fg run clear @s *[minecraft:custom_data~{echo_tag:2b}]
scoreboard players operation #n rpg_fg *= #3 rpg_fg
execute store result storage rpg:forge cv.n int 1 run scoreboard players get #n rpg_fg
function rpg:forge/conv/give_soul with storage rpg:forge cv
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　旧材料换成了新的养成材料","color":"#AAAAAA","italic":false}]
