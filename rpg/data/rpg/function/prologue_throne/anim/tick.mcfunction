# 座天使动画（as 载体）。rpg_prth_anim = 当前片段，rpg_prth_t = 已播放刻数。
execute unless score @s rpg_prth_anim matches 0.. run function rpg:prologue_throne/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_prth_mc 1
execute if score @s rpg_prth_mc matches 4.. run function rpg:prologue_throne/anim/stride
execute if score @s rpg_prth_anim matches 0 if score @s rpg_prth_mv matches 1.. run return run function rpg:prologue_throne/anim/enter/idle
execute if score @s rpg_prth_anim matches 0 if score @s rpg_prth_mv matches 0 run return run function rpg:prologue_throne/anim/enter/idle
execute if score @s rpg_prth_anim matches 0 run return run function rpg:prologue_throne/anim/idle/tick
execute if score @s rpg_prth_anim matches 1 run return run function rpg:prologue_throne/anim/blink/tick
