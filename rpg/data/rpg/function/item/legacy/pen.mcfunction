# 风骨 · 着意：每次有效命中在黑、白二式之间轮转。
scoreboard players set @s rpg_leg_cd 5
execute if entity @s[scores={rpg_pen_mode=0}] run function rpg:item/legacy/pen_black
execute if entity @s[scores={rpg_pen_mode=1}] run function rpg:item/legacy/pen_white
