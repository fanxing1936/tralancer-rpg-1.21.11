execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.mis.part] run kill @s
tag @s remove rpg.mis
effect clear @s minecraft:invisibility
scoreboard players reset @s rpg_mis_anim
scoreboard players reset @s rpg_mis_t
scoreboard players reset @s rpg_mis_mv
scoreboard players reset @s rpg_mis_mc
scoreboard players reset @s rpg_mis_x
scoreboard players reset @s rpg_mis_z
