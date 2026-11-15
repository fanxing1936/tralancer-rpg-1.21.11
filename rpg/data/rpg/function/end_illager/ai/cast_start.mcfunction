# 圣光弹：转向最近的人，定身念咒
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..22,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rpg_ei_st 1
scoreboard players set @s rpg_ei_ta 0
function rpg:end_illager/anim/enter/cast
