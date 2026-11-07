# 挥戟：转向最近的目标，定身出手。
data merge entity @s {NoAI:1b}
execute facing entity @a[distance=..3.2,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rpg_tg_st 1
scoreboard players set @s rpg_tg_ta 0
function rpg:tower_guard/anim/enter/attack
