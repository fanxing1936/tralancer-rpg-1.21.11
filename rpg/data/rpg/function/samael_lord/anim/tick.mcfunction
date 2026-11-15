# 萨麦尔动画（as 载体）。rpg_sml_anim = 当前片段，rpg_sml_t = 已播放刻数。
execute unless score @s rpg_sml_anim matches 0.. run function rpg:samael_lord/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_sml_mc 1
execute if score @s rpg_sml_mc matches 4.. run function rpg:samael_lord/anim/stride
execute if score @s rpg_sml_anim matches 0 if score @s rpg_sml_mv matches 1.. run return run function rpg:samael_lord/anim/enter/walk
execute if score @s rpg_sml_anim matches 1 if score @s rpg_sml_mv matches 0 run return run function rpg:samael_lord/anim/enter/idle
execute if score @s rpg_sml_anim matches 0 run return run function rpg:samael_lord/anim/idle/tick
execute if score @s rpg_sml_anim matches 1 run return run function rpg:samael_lord/anim/walk/tick
execute if score @s rpg_sml_anim matches 2 run return run function rpg:samael_lord/anim/cast/tick
execute if score @s rpg_sml_anim matches 3 run return run function rpg:samael_lord/anim/charge/tick
execute if score @s rpg_sml_anim matches 4 run return run function rpg:samael_lord/anim/summon/tick
execute if score @s rpg_sml_anim matches 5 run return run function rpg:samael_lord/anim/super/tick
execute if score @s rpg_sml_anim matches 6 run return run function rpg:samael_lord/anim/rise/tick
