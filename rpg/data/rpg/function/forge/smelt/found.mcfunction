scoreboard players set #found rpg_fg 1
scoreboard players operation #me rpg_fg = @s rpg_fg_id
execute as @e[type=minecraft:marker,tag=rpg.fg.fire] if score @s rpg_fg_eo = #me rpg_fg run kill @s
execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fire","rpg.fg.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_eo = #me rpg_fg
tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new
