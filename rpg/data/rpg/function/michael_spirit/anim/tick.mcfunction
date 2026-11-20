# 米迦勒灵体动画（as 载体）。rpg_mis_anim = 当前片段，rpg_mis_t = 已播放刻数。
execute unless score @s rpg_mis_anim matches 0.. run function rpg:michael_spirit/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_mis_mc 1
execute if score @s rpg_mis_mc matches 4.. run function rpg:michael_spirit/anim/stride
execute if score @s rpg_mis_anim matches 6 if score @s rpg_mis_mv matches 1.. run return run function rpg:michael_spirit/anim/enter/rib_walk
execute if score @s rpg_mis_anim matches 7 if score @s rpg_mis_mv matches 0 run return run function rpg:michael_spirit/anim/enter/rib_idle
execute if score @s rpg_mis_anim matches 0 if score @s rpg_mis_mv matches 1.. run return run function rpg:michael_spirit/anim/enter/walk
execute if score @s rpg_mis_anim matches 1 if score @s rpg_mis_mv matches 0 run return run function rpg:michael_spirit/anim/enter/idle
execute if score @s rpg_mis_anim matches 0 run return run function rpg:michael_spirit/anim/idle/tick
execute if score @s rpg_mis_anim matches 1 run return run function rpg:michael_spirit/anim/walk/tick
execute if score @s rpg_mis_anim matches 2 run return run function rpg:michael_spirit/anim/run/tick
execute if score @s rpg_mis_anim matches 3 run return run function rpg:michael_spirit/anim/slash1/tick
execute if score @s rpg_mis_anim matches 4 run return run function rpg:michael_spirit/anim/slash2/tick
execute if score @s rpg_mis_anim matches 5 run return run function rpg:michael_spirit/anim/sweep/tick
execute if score @s rpg_mis_anim matches 6 run return run function rpg:michael_spirit/anim/rib_idle/tick
execute if score @s rpg_mis_anim matches 7 run return run function rpg:michael_spirit/anim/rib_walk/tick
execute if score @s rpg_mis_anim matches 8 run return run function rpg:michael_spirit/anim/rib_run/tick
execute if score @s rpg_mis_anim matches 9 run return run function rpg:michael_spirit/anim/rib_slash1/tick
execute if score @s rpg_mis_anim matches 10 run return run function rpg:michael_spirit/anim/rib_slash2/tick
execute if score @s rpg_mis_anim matches 11 run return run function rpg:michael_spirit/anim/rib_slash3/tick
execute if score @s rpg_mis_anim matches 12 run return run function rpg:michael_spirit/anim/rib_slash4/tick
execute if score @s rpg_mis_anim matches 13 run return run function rpg:michael_spirit/anim/rib_slash5/tick
execute if score @s rpg_mis_anim matches 14 run return run function rpg:michael_spirit/anim/rib_slash6/tick
execute if score @s rpg_mis_anim matches 15 run return run function rpg:michael_spirit/anim/roll_f/tick
execute if score @s rpg_mis_anim matches 16 run return run function rpg:michael_spirit/anim/roll_b/tick
execute if score @s rpg_mis_anim matches 17 run return run function rpg:michael_spirit/anim/roll_l/tick
execute if score @s rpg_mis_anim matches 18 run return run function rpg:michael_spirit/anim/roll_r/tick
execute if score @s rpg_mis_anim matches 19 run return run function rpg:michael_spirit/anim/hurt/tick
execute if score @s rpg_mis_anim matches 20 run return run function rpg:michael_spirit/anim/fall/tick
execute if score @s rpg_mis_anim matches 21 run return run function rpg:michael_spirit/anim/down/tick
