# 沿当前朝向补一支弩箭。方向取两个临时标记的坐标差，不用三角函数。
summon minecraft:marker ^ ^ ^ {Tags:["rpg.hc.o"]}
summon minecraft:marker ^ ^ ^1 {Tags:["rpg.hc.d"]}
summon minecraft:arrow ^ ^ ^0.6 {Tags:["rpg.hc.bolt","rpg.hc.new"],pickup:2b,crit:1b}
execute store result score #ox rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.o,limit=1] Pos[0] 1000
execute store result score #oy rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.o,limit=1] Pos[1] 1000
execute store result score #oz rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.o,limit=1] Pos[2] 1000
execute store result score #dx rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.d,limit=1] Pos[0] 1000
execute store result score #dy rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.d,limit=1] Pos[1] 1000
execute store result score #dz rpg_hc_tmp run data get entity @e[type=marker,tag=rpg.hc.d,limit=1] Pos[2] 1000
scoreboard players operation #dx rpg_hc_tmp -= #ox rpg_hc_tmp
scoreboard players operation #dy rpg_hc_tmp -= #oy rpg_hc_tmp
scoreboard players operation #dz rpg_hc_tmp -= #oz rpg_hc_tmp
execute as @e[type=arrow,tag=rpg.hc.new,limit=1] run function rpg:item/extra/harp_crossbow_aim
kill @e[type=marker,tag=rpg.hc.o]
kill @e[type=marker,tag=rpg.hc.d]
