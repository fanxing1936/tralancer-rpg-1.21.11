# 别西卜动画（as 载体）。rpg_bz_anim = 当前片段，rpg_bz_t = 已播放刻数。
execute unless score @s rpg_bz_anim matches 0.. run function rpg:beelzebub/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_bz_mc 1
execute if score @s rpg_bz_mc matches 4.. run function rpg:beelzebub/anim/stride
execute if score @s rpg_bz_anim matches 0 if score @s rpg_bz_mv matches 1.. run return run function rpg:beelzebub/anim/enter/walk
execute if score @s rpg_bz_anim matches 1 if score @s rpg_bz_mv matches 0 run return run function rpg:beelzebub/anim/enter/idle
execute if score @s rpg_bz_anim matches 0 run return run function rpg:beelzebub/anim/idle/tick
execute if score @s rpg_bz_anim matches 1 run return run function rpg:beelzebub/anim/walk/tick
execute if score @s rpg_bz_anim matches 2 run return run function rpg:beelzebub/anim/cast/tick
execute if score @s rpg_bz_anim matches 3 run return run function rpg:beelzebub/anim/summon/tick
execute if score @s rpg_bz_anim matches 4 run return run function rpg:beelzebub/anim/rise/tick
