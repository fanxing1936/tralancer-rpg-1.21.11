# 沿当前朝向射出一支箭（速度 1.6），Owner 取 storage rpg:forge owner。
summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.va"]}
summon minecraft:marker ^ ^ ^1 {Tags:["rpg.fg.vb"]}
execute store result score #ax rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.va,limit=1] Pos[0] 1000
execute store result score #ay rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.va,limit=1] Pos[1] 1000
execute store result score #az rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.va,limit=1] Pos[2] 1000
execute store result score #bx rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.vb,limit=1] Pos[0] 1000
execute store result score #by rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.vb,limit=1] Pos[1] 1000
execute store result score #bz rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.vb,limit=1] Pos[2] 1000
scoreboard players operation #bx rpg_fg -= #ax rpg_fg
scoreboard players operation #by rpg_fg -= #ay rpg_fg
scoreboard players operation #bz rpg_fg -= #az rpg_fg
summon minecraft:arrow ^ ^ ^0.9 {Tags:["rpg.fg.na","rpg.fg.a"],pickup:0b,damage:3.0d}
execute store result entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Motion[0] double 0.0016 run scoreboard players get #bx rpg_fg
execute store result entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Motion[1] double 0.0016 run scoreboard players get #by rpg_fg
execute store result entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Motion[2] double 0.0016 run scoreboard players get #bz rpg_fg
data modify entity @e[type=minecraft:arrow,tag=rpg.fg.na,limit=1] Owner set from storage rpg:forge owner
tag @e[type=minecraft:arrow,tag=rpg.fg.na] remove rpg.fg.na
kill @e[type=minecraft:marker,tag=rpg.fg.va]
kill @e[type=minecraft:marker,tag=rpg.fg.vb]
particle minecraft:crit ~ ~ ~ 0.1 0.1 0.1 0.2 4
