# 没走过去：回一成血再打一轮；第三次直接进结局
scoreboard players add @s rpg_dt_dsp 1
execute if score @s rpg_dt_dsp matches 3.. run return run function rpg:daath_fight/despair/met
tag @s remove rpg.dt.desp
tag @s remove rpg.dt.mute
scoreboard players set @s rpg_dt_bgm 0
function rpg:daath_fight/sk/end
function rpg:daath_fight/despair/heal
function rpg:daath/anim/enter/idle
scoreboard players set @s rpg_dt_gap 20
