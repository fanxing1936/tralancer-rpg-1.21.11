scoreboard players set @s rpg_mk_ws 0
execute store result score @s rpg_mk_wt run random value 0..12
function rpg:watchling/anim/enter/idle
