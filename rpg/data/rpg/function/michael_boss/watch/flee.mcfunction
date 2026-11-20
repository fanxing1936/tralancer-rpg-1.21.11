# 受击传送（as/at 它）：往后 6 格
function rpg:michael_boss/vfx/blink
execute positioned ^ ^ ^-6 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
scoreboard players set @s rpg_mk_ws 2
scoreboard players set @s rpg_mk_wt 0
function rpg:watchling/anim/enter/tp_in
execute at @s run function rpg:michael_boss/vfx/blink
