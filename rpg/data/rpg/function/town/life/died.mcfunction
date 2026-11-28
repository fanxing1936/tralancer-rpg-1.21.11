scoreboard players set @s rpg_tl_dc 0
execute unless entity @s[tag=rpg.tl.holy] run return 0
execute store result storage rpg:town k.id int 1 run scoreboard players get @s rpg_fg_id
execute as @e[type=minecraft:item,distance=..6] run function rpg:town/life/keep with storage rpg:town k
tag @s add rpg.tl.kept
