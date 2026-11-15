execute if score @s rpg_ub matches 2 run function rpg:usurper_boss/s2/scale
execute store result score @s rpg_ub_h run data get entity @s Health 1
execute store result bossbar rpg:usurper_boss value run scoreboard players get @s rpg_ub_h
# 横幅每 50 血一档，跨档才换图；变身期间停在空条
execute if entity @s[tag=rpg.usb.morph] run return 0
scoreboard players operation #s rpg_ub = @s rpg_ub_h
scoreboard players add #s rpg_ub 49
scoreboard players set #k rpg_ub 50
scoreboard players operation #s rpg_ub /= #k rpg_ub
execute if score #s rpg_ub matches 21.. run scoreboard players set #s rpg_ub 20
execute if score #s rpg_ub matches ..-1 run scoreboard players set #s rpg_ub 0
execute unless score #s rpg_ub = @s rpg_ub_s run function rpg:usurper_boss/bar_name
