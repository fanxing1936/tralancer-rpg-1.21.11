# 教皇动画（as 载体）。rpg_pp_anim = 当前片段，rpg_pp_t = 已播放刻数。
execute unless score @s rpg_pp_anim matches 0.. run function rpg:pope/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_pp_mc 1
execute if score @s rpg_pp_mc matches 4.. run function rpg:pope/anim/stride
execute if score @s rpg_pp_anim matches 0 if score @s rpg_pp_mv matches 1.. run return run function rpg:pope/anim/enter/walk
execute if score @s rpg_pp_anim matches 1 if score @s rpg_pp_mv matches 0 run return run function rpg:pope/anim/enter/idle
execute if score @s rpg_pp_anim matches 0 run return run function rpg:pope/anim/idle/tick
execute if score @s rpg_pp_anim matches 1 run return run function rpg:pope/anim/walk/tick
execute if score @s rpg_pp_anim matches 2 run return run function rpg:pope/anim/attack/tick
execute if score @s rpg_pp_anim matches 3 run return run function rpg:pope/anim/summon/tick
execute if score @s rpg_pp_anim matches 4 run return run function rpg:pope/anim/cast/tick
execute if score @s rpg_pp_anim matches 5 run return run function rpg:pope/anim/appear/tick
execute if score @s rpg_pp_anim matches 6 run return run function rpg:pope/anim/teleport_in/tick
execute if score @s rpg_pp_anim matches 7 run return run function rpg:pope/anim/teleport_out/tick
execute if score @s rpg_pp_anim matches 8 run return run function rpg:pope/anim/whirlwind/tick
