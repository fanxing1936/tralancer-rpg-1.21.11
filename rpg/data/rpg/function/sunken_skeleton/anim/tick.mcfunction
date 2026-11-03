# 沉没罪仆动画（as 载体）。rpg_sk_anim = 当前片段，rpg_sk_t = 已播放刻数。
execute unless score @s rpg_sk_anim matches 0.. run function rpg:sunken_skeleton/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_sk_mc 1
execute if score @s rpg_sk_mc matches 4.. run function rpg:sunken_skeleton/anim/stride
execute if score @s rpg_sk_anim matches 0 if score @s rpg_sk_mv matches 1.. run return run function rpg:sunken_skeleton/anim/enter/walk
execute if score @s rpg_sk_anim matches 1 if score @s rpg_sk_mv matches 0 run return run function rpg:sunken_skeleton/anim/enter/idle
execute if score @s rpg_sk_anim matches 0 run return run function rpg:sunken_skeleton/anim/idle/tick
execute if score @s rpg_sk_anim matches 1 run return run function rpg:sunken_skeleton/anim/walk/tick
execute if score @s rpg_sk_anim matches 2 run return run function rpg:sunken_skeleton/anim/attack/tick
execute if score @s rpg_sk_anim matches 3 run return run function rpg:sunken_skeleton/anim/shoot/tick
