# 被贴身：背向最近的人瞬移 8 格，落在地面上
scoreboard players set @s rpg_ei_bc 100
particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40 normal
playsound rpg:end_illager.blink hostile @a[distance=..24] ~ ~ ~ 1 1
execute facing entity @e[tag=rpg.unit.f,distance=..5,sort=nearest,limit=1] feet rotated ~ 0 positioned ^ ^ ^-8 positioned over motion_blocking_no_leaves if block ~ ~1 ~ #minecraft:replaceable run tp @s ~ ~ ~ ~180 0
execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40 normal
function rpg:end_illager/anim/enter/rise
