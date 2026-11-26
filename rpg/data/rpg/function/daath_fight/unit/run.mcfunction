# 有挑战者在场才动
scoreboard players add @s rpg_dt_orb 1
execute if entity @s[y=64.4,dy=60,tag=!rpg.dt.hid] run tp @s ~ 64 ~
execute unless entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..26] run function rpg:daath_fight/unit/home
execute if entity @s[tag=rpg.dt.end] run return run function rpg:daath_fight/end/tick
function rpg:daath_fight/unit/light
function rpg:daath_fight/unit/hp
function rpg:daath_fight/music/tick
execute if score @a[tag=rpg.dt.me,limit=1] rpg_dt_ph matches 4.. run return run function rpg:daath_fight/unit/idle
execute if entity @s[tag=rpg.dt.morph] run return run function rpg:daath_fight/morph/tick
execute if entity @s[tag=rpg.dt.desp] run return run function rpg:daath_fight/despair/tick
execute if score @s rpg_dt_h matches ..15 if score @s rpg_dt_st matches 1 run return run function rpg:daath_fight/stage/end1
execute if score @s rpg_dt_h matches ..15 if score @s rpg_dt_st matches 2 run return run function rpg:daath_fight/stage/end2
function rpg:daath_fight/mind/watch
function rpg:daath_fight/steal/clock
execute if score @s rpg_dt_blade matches 1.. run function rpg:daath_fight/unit/blade
execute if score @s rpg_dt_sk matches 1.. run return run function rpg:daath_fight/sk/tick
function rpg:daath_fight/schedule
