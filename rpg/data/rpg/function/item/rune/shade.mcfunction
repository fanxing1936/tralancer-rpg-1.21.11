execute as @a[tag=rpg.h.shade_tag1,scores={rpg_shade=40..}] at @s run function rpg:item/rune/shade_burst
execute as @a[scores={rpg_shade=1..}] unless entity @s[tag=rpg.h.shade_tag1] run scoreboard players set @s rpg_shade 0
