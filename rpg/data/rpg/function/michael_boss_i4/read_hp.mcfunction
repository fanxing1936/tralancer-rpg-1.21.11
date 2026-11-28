tp @e[type=minecraft:marker,tag=rpg.mkb.last,limit=1,distance=0..] @s
execute store result score @s rpg_mk_h run data get entity @s Health 1
execute store result bossbar rpg:michael_boss_i4 value run scoreboard players get @s rpg_mk_h
execute if entity @s[tag=rpg.mkb.morph] run return 0
scoreboard players operation #s rpg_mk_i4 = @s rpg_mk_h
scoreboard players add #s rpg_mk_i4 59
scoreboard players set #k rpg_mk_i4 60
scoreboard players operation #s rpg_mk_i4 /= #k rpg_mk_i4
execute if score #s rpg_mk_i4 matches 21.. run scoreboard players set #s rpg_mk_i4 20
execute if score #s rpg_mk_i4 matches ..-1 run scoreboard players set #s rpg_mk_i4 0
execute unless score #s rpg_mk_i4 = @s rpg_mk_s run function rpg:michael_boss_i4/bar_name
