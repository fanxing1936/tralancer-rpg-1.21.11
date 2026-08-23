# 钉影［被动］—— 箭矢命中后把目标钉在原地。
execute as @e[type=minecraft:arrow,tag=!rpg.rune.pin] on origin if entity @s[tag=rpg.h.pin_tag1] at @s run tag @e[type=minecraft:arrow,distance=0..2] add rpg.rune.pin
execute if entity @e[tag=rpg.rune.pin] run function rpg:item/rune/pin/g0
