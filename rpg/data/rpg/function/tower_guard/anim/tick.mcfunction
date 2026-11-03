# 圣卫动画（as 载体）。rpg_tg_anim = 当前片段，rpg_tg_t = 已播放刻数。
execute unless score @s rpg_tg_anim matches 0.. run function rpg:tower_guard/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_tg_mc 1
execute if score @s rpg_tg_mc matches 4.. run function rpg:tower_guard/anim/stride
execute if score @s rpg_tg_anim matches 0 if score @s rpg_tg_mv matches 1.. run return run function rpg:tower_guard/anim/enter/walk
execute if score @s rpg_tg_anim matches 1 if score @s rpg_tg_mv matches 0 run return run function rpg:tower_guard/anim/enter/idle
execute if score @s rpg_tg_anim matches 0 run return run function rpg:tower_guard/anim/idle/tick
execute if score @s rpg_tg_anim matches 1 run return run function rpg:tower_guard/anim/walk/tick
execute if score @s rpg_tg_anim matches 2 run return run function rpg:tower_guard/anim/attack/tick
execute if score @s rpg_tg_anim matches 3 run return run function rpg:tower_guard/anim/charge/tick
execute if score @s rpg_tg_anim matches 4 run return run function rpg:tower_guard/anim/normal_stop/tick
execute if score @s rpg_tg_anim matches 5 run return run function rpg:tower_guard/anim/collide_stop/tick
execute if score @s rpg_tg_anim matches 6 run return run function rpg:tower_guard/anim/shield_break/tick
execute if score @s rpg_tg_anim matches 7 run return run function rpg:tower_guard/anim/stun/tick
