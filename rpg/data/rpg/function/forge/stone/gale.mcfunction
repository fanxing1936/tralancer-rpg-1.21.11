execute rotated ~ 0 positioned ^ ^ ^2.5 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.gale","rpg.fg.new"]}
execute rotated ~ 0 run tp @e[type=minecraft:marker,tag=rpg.fg.new,limit=1] ^ ^ ^2.5 ~ 0
scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_t 80
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_eo = @s rpg_fg_id
tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new
playsound minecraft:entity.breeze.wind_burst player @a[distance=..24] ~ ~ ~ 1 0.8
