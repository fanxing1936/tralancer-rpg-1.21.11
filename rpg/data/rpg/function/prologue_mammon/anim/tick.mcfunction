# 玛门（序章）动画（as 载体）。rpg_prmm_anim = 当前片段，rpg_prmm_t = 已播放刻数。
execute unless score @s rpg_prmm_anim matches 0.. run function rpg:prologue_mammon/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_prmm_mc 1
execute if score @s rpg_prmm_mc matches 4.. run function rpg:prologue_mammon/anim/stride
execute if score @s rpg_prmm_anim matches 0 if score @s rpg_prmm_mv matches 1.. run return run function rpg:prologue_mammon/anim/enter/walk
execute if score @s rpg_prmm_anim matches 1 if score @s rpg_prmm_mv matches 0 run return run function rpg:prologue_mammon/anim/enter/idle
execute if score @s rpg_prmm_anim matches 0 run return run function rpg:prologue_mammon/anim/idle/tick
execute if score @s rpg_prmm_anim matches 1 run return run function rpg:prologue_mammon/anim/walk/tick
execute if score @s rpg_prmm_anim matches 2 run return run function rpg:prologue_mammon/anim/run/tick
execute if score @s rpg_prmm_anim matches 3 run return run function rpg:prologue_mammon/anim/talk/tick
execute if score @s rpg_prmm_anim matches 4 run return run function rpg:prologue_mammon/anim/flee/tick
execute if score @s rpg_prmm_anim matches 5 run return run function rpg:prologue_mammon/anim/fold/tick
execute if score @s rpg_prmm_anim matches 6 run return run function rpg:prologue_mammon/anim/stun/tick
execute if score @s rpg_prmm_anim matches 7 run return run function rpg:prologue_mammon/anim/hurt/tick
execute if score @s rpg_prmm_anim matches 8 run return run function rpg:prologue_mammon/anim/roll_b/tick
execute if score @s rpg_prmm_anim matches 9 run return run function rpg:prologue_mammon/anim/roll_f/tick
execute if score @s rpg_prmm_anim matches 10 run return run function rpg:prologue_mammon/anim/land/tick
execute if score @s rpg_prmm_anim matches 11 run return run function rpg:prologue_mammon/anim/kneel_down/tick
execute if score @s rpg_prmm_anim matches 12 run return run function rpg:prologue_mammon/anim/kneel_idle/tick
execute if score @s rpg_prmm_anim matches 13 run return run function rpg:prologue_mammon/anim/kneel_up/tick
execute if score @s rpg_prmm_anim matches 14 run return run function rpg:prologue_mammon/anim/bow/tick
execute if score @s rpg_prmm_anim matches 15 run return run function rpg:prologue_mammon/anim/look_up/tick
execute if score @s rpg_prmm_anim matches 16 run return run function rpg:prologue_mammon/anim/shield/tick
execute if score @s rpg_prmm_anim matches 17 run return run function rpg:prologue_mammon/anim/showoff/tick
execute if score @s rpg_prmm_anim matches 18 run return run function rpg:prologue_mammon/anim/hero/tick
execute if score @s rpg_prmm_anim matches 19 run return run function rpg:prologue_mammon/anim/twirl/tick
