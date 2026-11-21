scoreboard players operation #t rpg_fg = @s rpg_fg_eo
execute as @a if score @s rpg_fg_id = #t rpg_fg run tag @s add rpg.fg.eo
execute as @e[type=!#rpg:no_damage_track,type=!minecraft:player,type=!minecraft:armor_stand,tag=!rpg.unit,distance=..3,tag=!rpg.ally] run damage @s 4 rpg:forge_bonus by @a[tag=rpg.fg.eo,limit=1]
tag @a[tag=rpg.fg.eo] remove rpg.fg.eo
particle minecraft:explosion ~ ~0.3 ~ 0.6 0.2 0.6 0 3
particle minecraft:end_rod ~ ~0.5 ~ 0.4 0.6 0.4 0.15 16
playsound minecraft:entity.firework_rocket.blast player @a[distance=..24] ~ ~ ~ 1 0.7
kill @s
