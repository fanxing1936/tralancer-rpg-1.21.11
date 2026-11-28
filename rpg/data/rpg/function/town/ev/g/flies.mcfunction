# 一波蝇群（2 + 人数）
scoreboard players operation #k rpg_te = #np rpg_te
scoreboard players add #k rpg_te 2
execute as @e[type=minecraft:marker,tag=rpg.tw.in.granary] if score @s rpg_tw_id = #run rpg_te at @s run function rpg:town/ev/g/fly_n
