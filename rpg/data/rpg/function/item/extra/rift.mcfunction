# 疾风迸发之弓［裂空］
# 箭矢命中处炸开一道风的裂隙，把周围三格内的一切掀上天并造成风压伤害。
execute as @e[type=minecraft:arrow,tag=!rpg.rift] on origin if entity @s[tag=rpg.h.rift_tag1] at @s run tag @e[type=minecraft:arrow,distance=0..2] add rpg.rift
execute if entity @e[tag=rpg.rift] run function rpg:item/extra/rift/g0
