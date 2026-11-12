# 路西法·二阶段动画（as 载体）。rpg_lu2_anim = 当前片段，rpg_lu2_t = 已播放刻数。
execute unless score @s rpg_lu2_anim matches 0.. run function rpg:lucifer_p2/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_lu2_mc 1
execute if score @s rpg_lu2_mc matches 4.. run function rpg:lucifer_p2/anim/stride
execute if score @s rpg_lu2_anim matches 0 if score @s rpg_lu2_mv matches 1.. run return run function rpg:lucifer_p2/anim/enter/jungleabomination_walk
execute if score @s rpg_lu2_anim matches 1 if score @s rpg_lu2_mv matches 0 run return run function rpg:lucifer_p2/anim/enter/jungleabomination_idle
execute if score @s rpg_lu2_anim matches 0 run return run function rpg:lucifer_p2/anim/jungleabomination_idle/tick
execute if score @s rpg_lu2_anim matches 1 run return run function rpg:lucifer_p2/anim/jungleabomination_walk/tick
execute if score @s rpg_lu2_anim matches 2 run return run function rpg:lucifer_p2/anim/jungleabomination_attack/tick
execute if score @s rpg_lu2_anim matches 3 run return run function rpg:lucifer_p2/anim/jungleabomination_death/tick
execute if score @s rpg_lu2_anim matches 4 run return run function rpg:lucifer_p2/anim/jungleabomination_fall/tick
execute if score @s rpg_lu2_anim matches 5 run return run function rpg:lucifer_p2/anim/jungleabomination_land/tick
execute if score @s rpg_lu2_anim matches 6 run return run function rpg:lucifer_p2/anim/jungleabomination_projectileattack/tick
execute if score @s rpg_lu2_anim matches 7 run return run function rpg:lucifer_p2/anim/jungleabomination_projectileattack_end/tick
execute if score @s rpg_lu2_anim matches 8 run return run function rpg:lucifer_p2/anim/jungleabomination_projectileattack_loop/tick
execute if score @s rpg_lu2_anim matches 9 run return run function rpg:lucifer_p2/anim/jungleabomination_projectileattack_start/tick
execute if score @s rpg_lu2_anim matches 10 run return run function rpg:lucifer_p2/anim/jungleabomination_summon/tick
execute if score @s rpg_lu2_anim matches 11 run return run function rpg:lucifer_p2/anim/jungleabomination_vineattack/tick
execute if score @s rpg_lu2_anim matches 12 run return run function rpg:lucifer_p2/anim/jungleabomination_vineattackidle/tick
execute if score @s rpg_lu2_anim matches 13 run return run function rpg:lucifer_p2/anim/jungleabomination_vineattacksucessful/tick
execute if score @s rpg_lu2_anim matches 14 run return run function rpg:lucifer_p2/anim/jungleabomination_vineattackunsucessful/tick
execute if score @s rpg_lu2_anim matches 15 run return run function rpg:lucifer_p2/anim/jungleabomination_vulnerablefall/tick
execute if score @s rpg_lu2_anim matches 16 run return run function rpg:lucifer_p2/anim/jungleabomination_vulnerablegetup/tick
execute if score @s rpg_lu2_anim matches 17 run return run function rpg:lucifer_p2/anim/jungleabomination_vulnerablestuncycle/tick
