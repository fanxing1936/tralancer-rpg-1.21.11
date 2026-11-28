tp @e[type=minecraft:marker,tag=rpg.mkb.last,limit=1,predicate=!rpg:in_prologue] @s
execute store result score @s rpg_mk_h run data get entity @s Health 1
execute store result bossbar rpg:michael_boss value run scoreboard players get @s rpg_mk_h
execute if entity @s[tag=rpg.mkb.morph] run return 0
scoreboard players operation #s rpg_mk = @s rpg_mk_h
scoreboard players add #s rpg_mk 59
scoreboard players set #k rpg_mk 60
scoreboard players operation #s rpg_mk /= #k rpg_mk
execute if score #s rpg_mk matches 21.. run scoreboard players set #s rpg_mk 20
execute if score #s rpg_mk matches ..-1 run scoreboard players set #s rpg_mk 0
execute unless score #s rpg_mk = @s rpg_mk_s run function rpg:michael_boss/bar_name
