# 焰墙往外走（as/at 圆心）：半径 = (61 - 生命) × 0.508；两侧各 0.7 格内、脚着地、这道墙还没烧过的人挨一下
scoreboard players set #lo rpg_mk 61
scoreboard players operation #lo rpg_mk -= @s rpg_mk_life
scoreboard players set #k rpg_mk 508
scoreboard players operation #lo rpg_mk *= #k rpg_mk
scoreboard players operation #hi rpg_mk = #lo rpg_mk
scoreboard players remove #lo rpg_mk 700
scoreboard players add #hi rpg_mk 700
execute if score #lo rpg_mk matches ..-1 run scoreboard players set #lo rpg_mk 0
execute store result storage rpg:michael_boss wave.lo double 0.001 run scoreboard players get #lo rpg_mk
execute store result storage rpg:michael_boss wave.hi double 0.001 run scoreboard players get #hi rpg_mk
execute store result storage rpg:michael_boss wave.id int 1 run scoreboard players get @s rpg_mk_r
function rpg:michael_boss/sanctus/band with storage rpg:michael_boss wave
