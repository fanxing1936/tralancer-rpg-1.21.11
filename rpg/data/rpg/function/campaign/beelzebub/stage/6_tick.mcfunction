execute as @e[type=minecraft:marker,tag=rpg.ch1.cache1] at @s run function rpg:campaign/beelzebub/probe/cache1
execute as @e[type=minecraft:marker,tag=rpg.ch1.cache2] at @s run function rpg:campaign/beelzebub/probe/cache2
execute as @e[type=minecraft:marker,tag=rpg.ch1.cache3] at @s run function rpg:campaign/beelzebub/probe/cache3
execute if score @s rpg_ch1_obj matches 3.. run function rpg:campaign/beelzebub/advance
