# 冲锋：锁定此刻的方向，之后不再转向，所以可以侧身躲开，也可以引它撞墙。
data merge entity @s {NoAI:1b}
execute facing entity @a[distance=6..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rpg_tg_st 2
scoreboard players set @s rpg_tg_ta 0
function rpg:tower_guard/anim/enter/charge
