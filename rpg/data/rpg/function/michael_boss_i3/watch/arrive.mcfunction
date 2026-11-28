# 出现在最近那人身边（as 它）：四个方向里挑一个能站的
scoreboard players set @s rpg_mk_ws 2
scoreboard players set @s rpg_mk_wt 0
execute store result score #r rpg_mk_i3 run random value 0..3
execute if score #r rpg_mk_i3 matches 0 at @e[tag=rpg.unit.f,distance=..80,sort=nearest,limit=1] rotated ~0 0 positioned ^ ^ ^2.4 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score #r rpg_mk_i3 matches 1 at @e[tag=rpg.unit.f,distance=..80,sort=nearest,limit=1] rotated ~90 0 positioned ^ ^ ^2.4 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score #r rpg_mk_i3 matches 2 at @e[tag=rpg.unit.f,distance=..80,sort=nearest,limit=1] rotated ~180 0 positioned ^ ^ ^2.4 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute if score #r rpg_mk_i3 matches 3 at @e[tag=rpg.unit.f,distance=..80,sort=nearest,limit=1] rotated ~270 0 positioned ^ ^ ^2.4 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:watchling/anim/enter/tp_in
execute at @s run function rpg:michael_boss_i3/vfx/blink
