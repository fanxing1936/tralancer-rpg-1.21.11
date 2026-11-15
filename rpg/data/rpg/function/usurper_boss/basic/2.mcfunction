# 二阶段普攻（as/at 载体）：连拳三下，再跃起双拳砸地
execute unless entity @e[tag=rpg.unit.f,distance=..4.5] run return 0
scoreboard players set @s rpg_ub_sk 10
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 138
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..5.5,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:prime_enchanter/anim/enter/fury_fist
