# 砸锤：转向最近的人，定身出手
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..4.0,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rpg_rg_st 1
scoreboard players set @s rpg_rg_ta 0
function rpg:royal_guard/anim/enter/attack
