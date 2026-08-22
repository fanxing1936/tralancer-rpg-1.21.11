execute as @e[type=minecraft:arrow,tag=!hunter] on origin if entity @s[tag=rpg.h.hunter_tag1] at @s run effect give @s instant_damage 1 0 true
execute as @e[type=minecraft:arrow] on origin if entity @s[tag=rpg.h.hunter_tag1] at @s run tag @e[type=arrow,distance=0..2] add hunter
execute if entity @e[tag=hunter] run function rpg:item/bow/legend/hunter/hunter/g0





