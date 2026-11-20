execute store result score @s rpg_sl_h run data get entity @s Health 1
execute store result bossbar rpg:saul_boss value run scoreboard players get @s rpg_sl_h
execute if entity @s[tag=rpg.slb.morph] run return 0
scoreboard players operation #s rpg_sl = @s rpg_sl_h
scoreboard players add #s rpg_sl 49
scoreboard players set #k rpg_sl 50
scoreboard players operation #s rpg_sl /= #k rpg_sl
execute if score #s rpg_sl matches 21.. run scoreboard players set #s rpg_sl 20
execute if score #s rpg_sl matches ..-1 run scoreboard players set #s rpg_sl 0
execute unless score #s rpg_sl = @s rpg_sl_s run function rpg:saul_boss/bar_name
