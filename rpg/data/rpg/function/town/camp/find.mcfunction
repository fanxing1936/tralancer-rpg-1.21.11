# 找营地（positioned 营地中心 y=0，离镇约 200 格）：9 个候选，取高差最小的
scoreboard players set #best rpg_tw 9999
scoreboard players set #bn rpg_tw -1
function rpg:town/camp/c/0
function rpg:town/camp/c/1
function rpg:town/camp/c/2
function rpg:town/camp/c/3
function rpg:town/camp/c/4
function rpg:town/camp/c/5
function rpg:town/camp/c/6
function rpg:town/camp/c/7
function rpg:town/camp/c/8
execute if score #bn rpg_tw matches 0 run function rpg:town/camp/at/0
execute if score #bn rpg_tw matches 1 run function rpg:town/camp/at/1
execute if score #bn rpg_tw matches 2 run function rpg:town/camp/at/2
execute if score #bn rpg_tw matches 3 run function rpg:town/camp/at/3
execute if score #bn rpg_tw matches 4 run function rpg:town/camp/at/4
execute if score #bn rpg_tw matches 5 run function rpg:town/camp/at/5
execute if score #bn rpg_tw matches 6 run function rpg:town/camp/at/6
execute if score #bn rpg_tw matches 7 run function rpg:town/camp/at/7
execute if score #bn rpg_tw matches 8 run function rpg:town/camp/at/8
