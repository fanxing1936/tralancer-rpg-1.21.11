execute as @e[type=minecraft:arrow,tag=!bubble] on origin if entity @s[tag=rpg.h.bubble_tag1] at @s run effect give @s resistance 2 255 true
execute as @e[type=minecraft:arrow] on origin if entity @s[tag=rpg.h.bubble_tag1] at @s run tag @e[type=arrow,distance=0..2] add bubble
execute if entity @e[tag=bubble] run function rpg:item/bow/legend/bubble/bubble/g0




