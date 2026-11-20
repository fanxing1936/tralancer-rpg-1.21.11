# 扫罗动画（as 载体）。rpg_slm_anim = 当前片段，rpg_slm_t = 已播放刻数。
execute unless score @s rpg_slm_anim matches 0.. run function rpg:saul/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_slm_mc 1
execute if score @s rpg_slm_mc matches 4.. run function rpg:saul/anim/stride
execute if score @s rpg_slm_anim matches 0 if score @s rpg_slm_mv matches 1.. run return run function rpg:saul/anim/enter/walk
execute if score @s rpg_slm_anim matches 1 if score @s rpg_slm_mv matches 0 run return run function rpg:saul/anim/enter/idle
execute if score @s rpg_slm_anim matches 0 run return run function rpg:saul/anim/idle/tick
execute if score @s rpg_slm_anim matches 1 run return run function rpg:saul/anim/walk/tick
execute if score @s rpg_slm_anim matches 2 run return run function rpg:saul/anim/run/tick
execute if score @s rpg_slm_anim matches 3 run return run function rpg:saul/anim/thrust/tick
execute if score @s rpg_slm_anim matches 4 run return run function rpg:saul/anim/left/tick
execute if score @s rpg_slm_anim matches 5 run return run function rpg:saul/anim/right/tick
execute if score @s rpg_slm_anim matches 6 run return run function rpg:saul/anim/double/tick
execute if score @s rpg_slm_anim matches 7 run return run function rpg:saul/anim/final/tick
execute if score @s rpg_slm_anim matches 8 run return run function rpg:saul/anim/roll_f/tick
execute if score @s rpg_slm_anim matches 9 run return run function rpg:saul/anim/roll_b/tick
execute if score @s rpg_slm_anim matches 10 run return run function rpg:saul/anim/roll_l/tick
execute if score @s rpg_slm_anim matches 11 run return run function rpg:saul/anim/roll_r/tick
execute if score @s rpg_slm_anim matches 12 run return run function rpg:saul/anim/mighty/tick
execute if score @s rpg_slm_anim matches 13 run return run function rpg:saul/anim/twirl/tick
execute if score @s rpg_slm_anim matches 14 run return run function rpg:saul/anim/shadow/tick
execute if score @s rpg_slm_anim matches 15 run return run function rpg:saul/anim/kneel/tick
execute if score @s rpg_slm_anim matches 16 run return run function rpg:saul/anim/hero/tick
execute if score @s rpg_slm_anim matches 17 run return run function rpg:saul/anim/web/tick
execute if score @s rpg_slm_anim matches 18 run return run function rpg:saul/anim/showoff/tick
execute if score @s rpg_slm_anim matches 19 run return run function rpg:saul/anim/vanish/tick
execute if score @s rpg_slm_anim matches 20 run return run function rpg:saul/anim/land/tick
execute if score @s rpg_slm_anim matches 21 run return run function rpg:saul/anim/stun/tick
execute if score @s rpg_slm_anim matches 22 run return run function rpg:saul/anim/hurt/tick
execute if score @s rpg_slm_anim matches 23 run return run function rpg:saul/anim/fall/tick
execute if score @s rpg_slm_anim matches 24 run return run function rpg:saul/anim/down/tick
