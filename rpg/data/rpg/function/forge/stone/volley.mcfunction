scoreboard players set #i rpg_fg 48
execute anchored eyes positioned ^ ^ ^ run function rpg:forge/stone/volley_ray
data modify entity @e[type=minecraft:marker,tag=rpg.fg.new,limit=1] data.owner set from entity @s UUID
scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_t 60
tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new
playsound minecraft:item.crossbow.loading_end player @a[distance=..16] ~ ~ ~ 1 0.7
