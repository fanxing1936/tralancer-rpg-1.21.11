execute as @e[type=minecraft:armor_stand,tag=rpg.he] at @s run function rpg:heart_of_ender/follow
execute as @e[type=minecraft:item_display,tag=rpg.he.part] unless predicate rpg:heart_of_ender/riding run kill @s
