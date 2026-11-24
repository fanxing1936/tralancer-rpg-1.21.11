# 路西法（序章）动画（as 载体）。rpg_prlu_anim = 当前片段，rpg_prlu_t = 已播放刻数。
execute unless score @s rpg_prlu_anim matches 0.. run function rpg:prologue_lucifer/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_prlu_mc 1
execute if score @s rpg_prlu_mc matches 4.. run function rpg:prologue_lucifer/anim/stride
execute if score @s rpg_prlu_anim matches 0 if score @s rpg_prlu_mv matches 1.. run return run function rpg:prologue_lucifer/anim/enter/walk
execute if score @s rpg_prlu_anim matches 1 if score @s rpg_prlu_mv matches 0 run return run function rpg:prologue_lucifer/anim/enter/idle
execute if score @s rpg_prlu_anim matches 0 run return run function rpg:prologue_lucifer/anim/idle/tick
execute if score @s rpg_prlu_anim matches 1 run return run function rpg:prologue_lucifer/anim/walk/tick
execute if score @s rpg_prlu_anim matches 2 run return run function rpg:prologue_lucifer/anim/run/tick
execute if score @s rpg_prlu_anim matches 3 run return run function rpg:prologue_lucifer/anim/address/tick
execute if score @s rpg_prlu_anim matches 4 run return run function rpg:prologue_lucifer/anim/look_up/tick
execute if score @s rpg_prlu_anim matches 5 run return run function rpg:prologue_lucifer/anim/seized/tick
execute if score @s rpg_prlu_anim matches 6 run return run function rpg:prologue_lucifer/anim/pierced/tick
execute if score @s rpg_prlu_anim matches 7 run return run function rpg:prologue_lucifer/anim/tear/tick
execute if score @s rpg_prlu_anim matches 8 run return run function rpg:prologue_lucifer/anim/reach/tick
execute if score @s rpg_prlu_anim matches 9 run return run function rpg:prologue_lucifer/anim/stomped/tick
execute if score @s rpg_prlu_anim matches 10 run return run function rpg:prologue_lucifer/anim/pit_rise/tick
