# 贝利尔（序章）动画（as 载体）。rpg_prbl_anim = 当前片段，rpg_prbl_t = 已播放刻数。
execute unless score @s rpg_prbl_anim matches 0.. run function rpg:prologue_belial/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_prbl_mc 1
execute if score @s rpg_prbl_mc matches 4.. run function rpg:prologue_belial/anim/stride
execute if score @s rpg_prbl_anim matches 0 if score @s rpg_prbl_mv matches 1.. run return run function rpg:prologue_belial/anim/enter/walk
execute if score @s rpg_prbl_anim matches 1 if score @s rpg_prbl_mv matches 0 run return run function rpg:prologue_belial/anim/enter/idle
execute if score @s rpg_prbl_anim matches 0 run return run function rpg:prologue_belial/anim/idle/tick
execute if score @s rpg_prbl_anim matches 1 run return run function rpg:prologue_belial/anim/walk/tick
execute if score @s rpg_prbl_anim matches 2 run return run function rpg:prologue_belial/anim/run/tick
execute if score @s rpg_prbl_anim matches 3 run return run function rpg:prologue_belial/anim/talk/tick
execute if score @s rpg_prbl_anim matches 4 run return run function rpg:prologue_belial/anim/flee/tick
execute if score @s rpg_prbl_anim matches 5 run return run function rpg:prologue_belial/anim/fold/tick
execute if score @s rpg_prbl_anim matches 6 run return run function rpg:prologue_belial/anim/stun/tick
execute if score @s rpg_prbl_anim matches 7 run return run function rpg:prologue_belial/anim/hurt/tick
execute if score @s rpg_prbl_anim matches 8 run return run function rpg:prologue_belial/anim/roll_b/tick
execute if score @s rpg_prbl_anim matches 9 run return run function rpg:prologue_belial/anim/roll_f/tick
execute if score @s rpg_prbl_anim matches 10 run return run function rpg:prologue_belial/anim/land/tick
execute if score @s rpg_prbl_anim matches 11 run return run function rpg:prologue_belial/anim/kneel_down/tick
execute if score @s rpg_prbl_anim matches 12 run return run function rpg:prologue_belial/anim/kneel_idle/tick
execute if score @s rpg_prbl_anim matches 13 run return run function rpg:prologue_belial/anim/kneel_up/tick
execute if score @s rpg_prbl_anim matches 14 run return run function rpg:prologue_belial/anim/bow/tick
execute if score @s rpg_prbl_anim matches 15 run return run function rpg:prologue_belial/anim/look_up/tick
execute if score @s rpg_prbl_anim matches 16 run return run function rpg:prologue_belial/anim/shield/tick
execute if score @s rpg_prbl_anim matches 17 run return run function rpg:prologue_belial/anim/showoff/tick
execute if score @s rpg_prbl_anim matches 18 run return run function rpg:prologue_belial/anim/hero/tick
execute if score @s rpg_prbl_anim matches 19 run return run function rpg:prologue_belial/anim/twirl/tick
