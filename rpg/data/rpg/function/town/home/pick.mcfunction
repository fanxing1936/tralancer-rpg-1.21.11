# 抽故乡（as 玩家）：自己国家的两座镇里随机一座；没有国家就全大陆随机
execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
scoreboard players set #nat rpg_tw -1
function rpg:town/home/nation with storage rpg:onboard tmp
execute store result score #r rpg_tw run random value 0..1
scoreboard players operation @s rpg_tw_home = #nat rpg_tw
scoreboard players add @s rpg_tw_home 1
execute if score #r rpg_tw matches 1 run scoreboard players add @s rpg_tw_home 10
execute if score #nat rpg_tw matches -1 store result score @s rpg_tw_home run random value 1..20
