advancement revoke @s only rpg:item/wukong
execute as @s at @s run tp @s ^ ^ ^3 
execute as @s at @s run particle minecraft:gust_emitter_large ~ ~-1 ~
execute as @s at @s run particle end_rod ~0.2 ~ ~0.2 -0.4 0.1 -0.4 1 100
effect give @s slow_falling 1 255 true
execute as @s at @s run xp add @s -5 points 