# 空缺者：外表与常人无异的空壳。
# 新出现的村民里抽一部分标记，每刻只处理少量，避免村庄载入时集中掷点。
tag @e[type=minecraft:villager,tag=!rpg.vac.seen,limit=3] add rpg.vac.new
execute as @e[tag=rpg.vac.new] store result score @s rpg_vac run random value 1..6
execute as @e[tag=rpg.vac.new,scores={rpg_vac=1}] run tag @s add rpg.vacant
tag @e[tag=rpg.vac.new] add rpg.vac.seen
tag @e[tag=rpg.vac.new] remove rpg.vac.new
