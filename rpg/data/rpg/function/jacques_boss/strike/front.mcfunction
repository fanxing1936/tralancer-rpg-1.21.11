# 下劈（as/at 载体）：身前 2.3 格；金色弧光
execute positioned ^ ^ ^1.8 run tag @e[tag=rpg.unit.f,distance=..2.3] add rpg.jqb.hit
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit] run damage @s 7 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/pop
tag @e[tag=rpg.unit] remove rpg.jqb.hit
execute if score @s rpg_jq matches 1 run function rpg:jacques_boss/vfx/front1
execute if score @s rpg_jq matches 2 run function rpg:jacques_boss/vfx/front2
