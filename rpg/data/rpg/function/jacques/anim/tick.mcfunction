# 雅克动画（as 载体）。rpg_jqm_anim = 当前片段，rpg_jqm_t = 已播放刻数。
execute unless score @s rpg_jqm_anim matches 0.. run function rpg:jacques/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_jqm_mc 1
execute if score @s rpg_jqm_mc matches 4.. run function rpg:jacques/anim/stride
execute if score @s rpg_jqm_anim matches 0 if score @s rpg_jqm_mv matches 1.. run return run function rpg:jacques/anim/enter/walk
execute if score @s rpg_jqm_anim matches 1 if score @s rpg_jqm_mv matches 0 run return run function rpg:jacques/anim/enter/idle
execute if score @s rpg_jqm_anim matches 0 run return run function rpg:jacques/anim/idle/tick
execute if score @s rpg_jqm_anim matches 1 run return run function rpg:jacques/anim/walk/tick
execute if score @s rpg_jqm_anim matches 2 run return run function rpg:jacques/anim/run/tick
execute if score @s rpg_jqm_anim matches 3 run return run function rpg:jacques/anim/slash1/tick
execute if score @s rpg_jqm_anim matches 4 run return run function rpg:jacques/anim/slash2/tick
execute if score @s rpg_jqm_anim matches 5 run return run function rpg:jacques/anim/sweep/tick
execute if score @s rpg_jqm_anim matches 6 run return run function rpg:jacques/anim/load/tick
execute if score @s rpg_jqm_anim matches 7 run return run function rpg:jacques/anim/charge/tick
execute if score @s rpg_jqm_anim matches 8 run return run function rpg:jacques/anim/shoot/tick
execute if score @s rpg_jqm_anim matches 9 run return run function rpg:jacques/anim/roll_f/tick
execute if score @s rpg_jqm_anim matches 10 run return run function rpg:jacques/anim/roll_b/tick
execute if score @s rpg_jqm_anim matches 11 run return run function rpg:jacques/anim/horn/tick
execute if score @s rpg_jqm_anim matches 12 run return run function rpg:jacques/anim/gong/tick
execute if score @s rpg_jqm_anim matches 13 run return run function rpg:jacques/anim/mighty/tick
execute if score @s rpg_jqm_anim matches 14 run return run function rpg:jacques/anim/showoff/tick
execute if score @s rpg_jqm_anim matches 15 run return run function rpg:jacques/anim/kneel/tick
execute if score @s rpg_jqm_anim matches 16 run return run function rpg:jacques/anim/hero/tick
execute if score @s rpg_jqm_anim matches 17 run return run function rpg:jacques/anim/leap/tick
execute if score @s rpg_jqm_anim matches 18 run return run function rpg:jacques/anim/land/tick
execute if score @s rpg_jqm_anim matches 19 run return run function rpg:jacques/anim/curse/tick
execute if score @s rpg_jqm_anim matches 20 run return run function rpg:jacques/anim/stun/tick
execute if score @s rpg_jqm_anim matches 21 run return run function rpg:jacques/anim/hurt/tick
execute if score @s rpg_jqm_anim matches 22 run return run function rpg:jacques/anim/fall/tick
execute if score @s rpg_jqm_anim matches 23 run return run function rpg:jacques/anim/down/tick
