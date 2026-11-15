# 蔚蓝追寻者［深潜］
# 箭矢拖着深海的水压飞行；命中生物时把目标向下拽入"深渊"并短暂锚定。
execute as @e[type=minecraft:arrow,tag=!rpg.deep] on origin if entity @s[tag=rpg.h.deep_seek_tag1] at @s run tag @e[type=minecraft:arrow,distance=0..2] add rpg.deep
execute if entity @e[tag=rpg.deep] run function rpg:item/extra/deep_seek/g0
