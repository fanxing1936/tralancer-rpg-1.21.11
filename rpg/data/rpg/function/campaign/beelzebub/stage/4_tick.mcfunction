execute as @e[type=minecraft:marker,tag=rpg.ch1.trail1] at @s run function rpg:campaign/beelzebub/probe/trail1
execute as @e[type=minecraft:marker,tag=rpg.ch1.trail2] at @s run function rpg:campaign/beelzebub/probe/trail2
execute as @e[type=minecraft:marker,tag=rpg.ch1.trail3] at @s run function rpg:campaign/beelzebub/probe/trail3
execute as @e[type=minecraft:marker,tag=rpg.ch1.trail4] at @s run function rpg:campaign/beelzebub/probe/trail4
execute if score @s rpg_ch1_obj matches 4.. unless entity @s[tag=rpg.ch1.recap.area] run function rpg:campaign/beelzebub/recap/area
execute if score @s rpg_ch1_obj matches 4.. if entity @s[tag=rpg.ch1.recap.area] if score @s rpg_ch1_time matches 100.. run function rpg:campaign/beelzebub/advance
