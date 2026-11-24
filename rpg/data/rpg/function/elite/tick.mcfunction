scoreboard players add #t rpg_el 1
execute if score #t rpg_el matches 10 run execute as @e[type=#rpg:elite_pool,tag=!rpg.el.seen] at @s run function rpg:elite/roll
execute as @e[type=minecraft:item_display,tag=rpg.el.bomb] at @s run function rpg:elite/a/7/check
execute if score #t rpg_el matches 20.. run function rpg:elite/sec
