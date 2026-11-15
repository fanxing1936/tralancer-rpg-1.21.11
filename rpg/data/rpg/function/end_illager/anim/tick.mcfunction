# 圣卫·术士动画（as 载体）。rpg_ei_anim = 当前片段，rpg_ei_t = 已播放刻数。
execute unless score @s rpg_ei_anim matches 0.. run function rpg:end_illager/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_ei_mc 1
execute if score @s rpg_ei_mc matches 4.. run function rpg:end_illager/anim/stride
execute if score @s rpg_ei_anim matches 0 if score @s rpg_ei_mv matches 1.. run return run function rpg:end_illager/anim/enter/walk
execute if score @s rpg_ei_anim matches 1 if score @s rpg_ei_mv matches 0 run return run function rpg:end_illager/anim/enter/idle
execute if score @s rpg_ei_anim matches 0 run return run function rpg:end_illager/anim/idle/tick
execute if score @s rpg_ei_anim matches 1 run return run function rpg:end_illager/anim/walk/tick
execute if score @s rpg_ei_anim matches 2 run return run function rpg:end_illager/anim/cast/tick
execute if score @s rpg_ei_anim matches 3 run return run function rpg:end_illager/anim/strong/tick
execute if score @s rpg_ei_anim matches 4 run return run function rpg:end_illager/anim/summon/tick
execute if score @s rpg_ei_anim matches 5 run return run function rpg:end_illager/anim/rise/tick
execute if score @s rpg_ei_anim matches 6 run return run function rpg:end_illager/anim/hurt/tick
execute if score @s rpg_ei_anim matches 7 run return run function rpg:end_illager/anim/stun/tick
