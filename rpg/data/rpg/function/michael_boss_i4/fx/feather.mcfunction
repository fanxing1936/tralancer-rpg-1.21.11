# 飞行的羽毛（as/at 它）：每刻 0.9 格；碰到人就扎上去
tp @s ^ ^ ^0.9
execute at @s run particle minecraft:flame ~ ~ ~ 0.05 0.05 0.05 0.01 1
scoreboard players operation #m rpg_mk_i4 = @s rpg_mk_life
scoreboard players set #k rpg_mk_i4 4
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 at @s run function rpg:michael_boss_i4/feather/trail
execute at @s if entity @e[tag=rpg.unit.f,distance=..1.1] run function rpg:michael_boss_i4/feather/hit
