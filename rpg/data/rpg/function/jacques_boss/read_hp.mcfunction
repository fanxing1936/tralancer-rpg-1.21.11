execute store result score @s rpg_jq_h run data get entity @s Health 1
execute store result bossbar rpg:jacques_boss value run scoreboard players get @s rpg_jq_h
# 横幅每 50 血一档，跨档才换图；变身期间停在空条
execute if entity @s[tag=rpg.jqb.morph] run return 0
scoreboard players operation #s rpg_jq = @s rpg_jq_h
scoreboard players add #s rpg_jq 49
scoreboard players set #k rpg_jq 50
scoreboard players operation #s rpg_jq /= #k rpg_jq
execute if score #s rpg_jq matches 21.. run scoreboard players set #s rpg_jq 20
execute if score #s rpg_jq matches ..-1 run scoreboard players set #s rpg_jq 0
execute unless score #s rpg_jq = @s rpg_jq_s run function rpg:jacques_boss/bar_name
