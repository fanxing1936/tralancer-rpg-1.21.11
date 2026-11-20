# 老战友的幻影动画（as 载体）。rpg_slgm_anim = 当前片段，rpg_slgm_t = 已播放刻数。
execute unless score @s rpg_slgm_anim matches 0.. run function rpg:saul_ghost/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_slgm_mc 1
execute if score @s rpg_slgm_mc matches 4.. run function rpg:saul_ghost/anim/stride
execute if score @s rpg_slgm_anim matches 0 if score @s rpg_slgm_mv matches 1.. run return run function rpg:saul_ghost/anim/enter/walk
execute if score @s rpg_slgm_anim matches 1 if score @s rpg_slgm_mv matches 0 run return run function rpg:saul_ghost/anim/enter/idle
execute if score @s rpg_slgm_anim matches 0 run return run function rpg:saul_ghost/anim/idle/tick
execute if score @s rpg_slgm_anim matches 1 run return run function rpg:saul_ghost/anim/walk/tick
execute if score @s rpg_slgm_anim matches 2 run return run function rpg:saul_ghost/anim/shadow/tick
execute if score @s rpg_slgm_anim matches 3 run return run function rpg:saul_ghost/anim/thrust/tick
execute if score @s rpg_slgm_anim matches 4 run return run function rpg:saul_ghost/anim/final/tick
execute if score @s rpg_slgm_anim matches 5 run return run function rpg:saul_ghost/anim/roll_f/tick
