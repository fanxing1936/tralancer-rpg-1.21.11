# 别西卜（序章）动画（as 载体）。rpg_prbz_anim = 当前片段，rpg_prbz_t = 已播放刻数。
execute unless score @s rpg_prbz_anim matches 0.. run function rpg:prologue_beelzebub/anim/init
# 每 4 刻量一次水平位移：走过 8/100 格以上记为在走，没走就回 idle
scoreboard players add @s rpg_prbz_mc 1
execute if score @s rpg_prbz_mc matches 4.. run function rpg:prologue_beelzebub/anim/stride
execute if score @s rpg_prbz_anim matches 0 if score @s rpg_prbz_mv matches 1.. run return run function rpg:prologue_beelzebub/anim/enter/walk
execute if score @s rpg_prbz_anim matches 1 if score @s rpg_prbz_mv matches 0 run return run function rpg:prologue_beelzebub/anim/enter/idle
execute if score @s rpg_prbz_anim matches 0 run return run function rpg:prologue_beelzebub/anim/idle/tick
execute if score @s rpg_prbz_anim matches 1 run return run function rpg:prologue_beelzebub/anim/walk/tick
execute if score @s rpg_prbz_anim matches 2 run return run function rpg:prologue_beelzebub/anim/run/tick
execute if score @s rpg_prbz_anim matches 3 run return run function rpg:prologue_beelzebub/anim/talk/tick
execute if score @s rpg_prbz_anim matches 4 run return run function rpg:prologue_beelzebub/anim/flee/tick
execute if score @s rpg_prbz_anim matches 5 run return run function rpg:prologue_beelzebub/anim/fold/tick
execute if score @s rpg_prbz_anim matches 6 run return run function rpg:prologue_beelzebub/anim/stun/tick
execute if score @s rpg_prbz_anim matches 7 run return run function rpg:prologue_beelzebub/anim/hurt/tick
execute if score @s rpg_prbz_anim matches 8 run return run function rpg:prologue_beelzebub/anim/roll_b/tick
execute if score @s rpg_prbz_anim matches 9 run return run function rpg:prologue_beelzebub/anim/roll_f/tick
execute if score @s rpg_prbz_anim matches 10 run return run function rpg:prologue_beelzebub/anim/land/tick
execute if score @s rpg_prbz_anim matches 11 run return run function rpg:prologue_beelzebub/anim/kneel_down/tick
execute if score @s rpg_prbz_anim matches 12 run return run function rpg:prologue_beelzebub/anim/kneel_idle/tick
execute if score @s rpg_prbz_anim matches 13 run return run function rpg:prologue_beelzebub/anim/kneel_up/tick
execute if score @s rpg_prbz_anim matches 14 run return run function rpg:prologue_beelzebub/anim/bow/tick
execute if score @s rpg_prbz_anim matches 15 run return run function rpg:prologue_beelzebub/anim/look_up/tick
execute if score @s rpg_prbz_anim matches 16 run return run function rpg:prologue_beelzebub/anim/shield/tick
