# 撞墙：卸下防御，这是输出窗口。
attribute @s minecraft:armor base set 0
scoreboard players set @s rpg_tg_st 4
scoreboard players set @s rpg_tg_ta 0
function rpg:tower_guard/anim/enter/collide_stop
