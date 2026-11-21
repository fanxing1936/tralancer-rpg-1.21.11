# 把 @s 从 rpg.fg.from 那里推开（玩家不推）。
execute if entity @s[type=minecraft:player] run return 0
execute at @s facing entity @e[tag=rpg.fg.from,limit=1] feet rotated ~ 0 positioned ^ ^ ^-1 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.vb"]}
execute store result score #ax rpg_fg run data get entity @s Pos[0] 1000
execute store result score #az rpg_fg run data get entity @s Pos[2] 1000
execute store result score #bx rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.vb,limit=1] Pos[0] 1000
execute store result score #bz rpg_fg run data get entity @e[type=minecraft:marker,tag=rpg.fg.vb,limit=1] Pos[2] 1000
kill @e[type=minecraft:marker,tag=rpg.fg.vb]
scoreboard players operation #bx rpg_fg -= #ax rpg_fg
scoreboard players operation #bz rpg_fg -= #az rpg_fg
execute store result entity @s Motion[0] double 0.0009 run scoreboard players get #bx rpg_fg
execute store result entity @s Motion[2] double 0.0009 run scoreboard players get #bz rpg_fg
data modify entity @s Motion[1] set value 0.42d
