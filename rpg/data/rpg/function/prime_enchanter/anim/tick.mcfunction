# 首席附魔师动画（as 载体）。rpg_pe_anim = 当前片段，rpg_pe_t = 已播放刻数。
execute unless score @s rpg_pe_anim matches 0.. run function rpg:prime_enchanter/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_pe_mc 1
execute if score @s rpg_pe_mc matches 4.. run function rpg:prime_enchanter/anim/stride
execute if score @s rpg_pe_anim matches 0 if score @s rpg_pe_mv matches 1.. run return run function rpg:prime_enchanter/anim/enter/walk
execute if score @s rpg_pe_anim matches 1 if score @s rpg_pe_mv matches 0 run return run function rpg:prime_enchanter/anim/enter/idle
execute if score @s rpg_pe_anim matches 0 run return run function rpg:prime_enchanter/anim/idle/tick
execute if score @s rpg_pe_anim matches 1 run return run function rpg:prime_enchanter/anim/walk/tick
execute if score @s rpg_pe_anim matches 2 run return run function rpg:prime_enchanter/anim/appear/tick
execute if score @s rpg_pe_anim matches 3 run return run function rpg:prime_enchanter/anim/death/tick
execute if score @s rpg_pe_anim matches 4 run return run function rpg:prime_enchanter/anim/forward_strike/tick
execute if score @s rpg_pe_anim matches 5 run return run function rpg:prime_enchanter/anim/fury_fist/tick
execute if score @s rpg_pe_anim matches 6 run return run function rpg:prime_enchanter/anim/launch/tick
execute if score @s rpg_pe_anim matches 7 run return run function rpg:prime_enchanter/anim/lightning_slam/tick
execute if score @s rpg_pe_anim matches 8 run return run function rpg:prime_enchanter/anim/overcharge/tick
execute if score @s rpg_pe_anim matches 9 run return run function rpg:prime_enchanter/anim/hurt/tick
execute if score @s rpg_pe_anim matches 10 run return run function rpg:prime_enchanter/anim/summon/tick
