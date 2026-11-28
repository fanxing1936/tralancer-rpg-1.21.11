scoreboard players set @s rpg_mk_wt 0
scoreboard players set @s rpg_mk_ws 3
execute if predicate rpg:michael_boss_i3/heavy run scoreboard players set @s rpg_mk_ws 4
execute if score @s rpg_mk_ws matches 3 run function rpg:watchling/anim/enter/attack
execute if score @s rpg_mk_ws matches 4 run function rpg:watchling/anim/enter/heavy
