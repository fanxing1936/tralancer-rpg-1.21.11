# 一张面容（at 地面，rotated 为朝向）。只有一段动作：升起、张嘴、沉下去。
function rpg:arch_visage/debug/spawn
tag @e[type=minecraft:armor_stand,tag=rpg.av,tag=!rpg.pf.face,distance=..1] add rpg.pf.chase
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.chase,tag=!rpg.pf.face,distance=..1] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[type=minecraft:armor_stand,tag=rpg.pf.chase,tag=!rpg.pf.face,distance=..1] rpg_pf_l 76
tag @e[type=minecraft:armor_stand,tag=rpg.pf.chase,tag=!rpg.pf.face,distance=..1] add rpg.pf.face
