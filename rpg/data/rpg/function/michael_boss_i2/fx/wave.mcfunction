# 焰墙往外走（as/at 圆心）：半径 = (61 - 生命) × 0.508；两侧各 0.7 格内、脚着地、这道墙还没烧过的人挨一下
scoreboard players set #lo rpg_mk_i2 61
scoreboard players operation #lo rpg_mk_i2 -= @s rpg_mk_life
scoreboard players set #k rpg_mk_i2 508
scoreboard players operation #lo rpg_mk_i2 *= #k rpg_mk_i2
scoreboard players operation #hi rpg_mk_i2 = #lo rpg_mk_i2
scoreboard players remove #lo rpg_mk_i2 700
scoreboard players add #hi rpg_mk_i2 700
execute if score #lo rpg_mk_i2 matches ..-1 run scoreboard players set #lo rpg_mk_i2 0
execute store result storage rpg:michael_boss_i2 wave.lo double 0.001 run scoreboard players get #lo rpg_mk_i2
execute store result storage rpg:michael_boss_i2 wave.hi double 0.001 run scoreboard players get #hi rpg_mk_i2
execute store result storage rpg:michael_boss_i2 wave.id int 1 run scoreboard players get @s rpg_mk_r
function rpg:michael_boss_i2/sanctus/band with storage rpg:michael_boss_i2 wave
