execute as @e[type=minecraft:marker,tag=rpg.ch1.anom1] at @s run function rpg:campaign/beelzebub/probe/anom1
execute as @e[type=minecraft:marker,tag=rpg.ch1.anom2] at @s run function rpg:campaign/beelzebub/probe/anom2
execute as @e[type=minecraft:marker,tag=rpg.ch1.anom3] at @s run function rpg:campaign/beelzebub/probe/anom3
execute if score @s rpg_ch1_obj matches 3.. unless entity @s[tag=rpg.ch1.recap.anomaly] run function rpg:campaign/beelzebub/recap/anomaly
execute if score @s rpg_ch1_obj matches 3.. if entity @s[tag=rpg.ch1.recap.anomaly] if score @s rpg_ch1_time matches 200.. run function rpg:campaign/beelzebub/advance
