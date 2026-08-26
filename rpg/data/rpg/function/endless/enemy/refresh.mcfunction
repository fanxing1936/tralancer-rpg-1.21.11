tag @e[tag=rpg.end.enemy] remove rpg.end.enemy.current
execute as @e[tag=rpg.end.enemy] if score @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id run tag @s add rpg.end.enemy.current
