# 守望者动画（as 载体）。rpg_mkwm_anim = 当前片段，rpg_mkwm_t = 已播放刻数。
execute unless score @s rpg_mkwm_anim matches 0.. run function rpg:watchling/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_mkwm_mc 1
execute if score @s rpg_mkwm_mc matches 4.. run function rpg:watchling/anim/stride
execute if score @s rpg_mkwm_anim matches 0 if score @s rpg_mkwm_mv matches 1.. run return run function rpg:watchling/anim/enter/walk
execute if score @s rpg_mkwm_anim matches 1 if score @s rpg_mkwm_mv matches 0 run return run function rpg:watchling/anim/enter/idle
execute if score @s rpg_mkwm_anim matches 0 run return run function rpg:watchling/anim/idle/tick
execute if score @s rpg_mkwm_anim matches 1 run return run function rpg:watchling/anim/walk/tick
execute if score @s rpg_mkwm_anim matches 2 run return run function rpg:watchling/anim/attack/tick
execute if score @s rpg_mkwm_anim matches 3 run return run function rpg:watchling/anim/heavy/tick
execute if score @s rpg_mkwm_anim matches 4 run return run function rpg:watchling/anim/tp_out/tick
execute if score @s rpg_mkwm_anim matches 5 run return run function rpg:watchling/anim/tp_in/tick
execute if score @s rpg_mkwm_anim matches 6 run return run function rpg:watchling/anim/stun/tick
