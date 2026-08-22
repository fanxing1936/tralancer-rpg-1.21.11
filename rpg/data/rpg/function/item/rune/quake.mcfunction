execute as @a[tag=rpg.h.quake_tag1,scores={rpg_quake=55..}] at @s run function rpg:item/rune/quake_burst
execute as @a[scores={rpg_quake=1..}] unless entity @s[tag=rpg.h.quake_tag1] run scoreboard players set @s rpg_quake 0
