# 空心人动画（as 载体）。rpg_tw_m12_anim = 当前片段，rpg_tw_m12_t = 已播放刻数。
execute unless score @s rpg_tw_m12_anim matches 0.. run function rpg:town_models/town_hollow/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_tw_m12_mc 1
execute if score @s rpg_tw_m12_mc matches 4.. run function rpg:town_models/town_hollow/anim/stride
execute if score @s rpg_tw_m12_anim matches 0 if score @s rpg_tw_m12_mv matches 1.. run return run function rpg:town_models/town_hollow/anim/enter/walk
execute if score @s rpg_tw_m12_anim matches 1 if score @s rpg_tw_m12_mv matches 0 run return run function rpg:town_models/town_hollow/anim/enter/idle
execute if score @s rpg_tw_m12_anim matches 0 run return run function rpg:town_models/town_hollow/anim/idle/tick
execute if score @s rpg_tw_m12_anim matches 1 run return run function rpg:town_models/town_hollow/anim/walk/tick
execute if score @s rpg_tw_m12_anim matches 2 run return run function rpg:town_models/town_hollow/anim/attack/tick
