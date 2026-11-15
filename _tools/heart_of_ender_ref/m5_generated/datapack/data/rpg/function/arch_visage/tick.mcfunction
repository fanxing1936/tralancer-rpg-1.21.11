execute as @e[type=minecraft:armor_stand,tag=rpg.av] at @s run function rpg:arch_visage/follow
execute as @e[type=minecraft:item_display,tag=rpg.av.part] unless predicate rpg:arch_visage/riding run kill @s
